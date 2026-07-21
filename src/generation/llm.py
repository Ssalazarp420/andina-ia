"""
Fase 5 - Generación de la respuesta final (inferencia del LLM).
"""

from src.config import settings
from src.generation.prompts import SYSTEM_PROMPT, build_cohere_documents, build_user_prompt


class ResponseGenerator:
    def __init__(self, provider: str | None = None):
        self.provider = provider or settings.LLM_PROVIDER
        self._client = self._init_client()

    def _init_client(self):
        if self.provider == "oci":
            try:
                import oci
                from oci.retry import NoneRetryStrategy

                config = oci.config.from_file(settings.OCI_CONFIG_FILE, settings.OCI_CONFIG_PROFILE)
                if settings.OCI_REGION:
                    config["region"] = settings.OCI_REGION

                from oci.generative_ai_inference import GenerativeAiInferenceClient

                return GenerativeAiInferenceClient(
                    config=config,
                    service_endpoint=settings.OCI_GENAI_INFERENCE_ENDPOINT,
                    retry_strategy=NoneRetryStrategy(),
                    timeout=(10, 240),
                )
            except Exception as exc:
                print(f"  ⚠️  No se pudo inicializar el cliente OCI Generative AI (chat): {exc}")
                return None

        if self.provider == "openai":
            from openai import OpenAI

            return OpenAI(api_key=settings.LLM_API_KEY)

        raise NotImplementedError(f"Proveedor de LLM no soportado aún: {self.provider}")

    @staticmethod
    def _build_serving_mode(oci_models_module):
        if settings.OCI_GENAI_CHAT_ENDPOINT_ID:
            return oci_models_module.DedicatedServingMode(endpoint_id=settings.OCI_GENAI_CHAT_ENDPOINT_ID)

        return oci_models_module.OnDemandServingMode(model_id=settings.OCI_GENAI_CHAT_MODEL_ID)

    def _call_oci_cohere(self, oci_models, question, retrieved_chunks, serving_mode):
        chat_request = oci_models.CohereChatRequest(
            message=question,
            preamble_override=SYSTEM_PROMPT,
            documents=build_cohere_documents(retrieved_chunks),
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=800,
            citation_quality=oci_models.CohereChatRequest.CITATION_QUALITY_ACCURATE,
            safety_mode=oci_models.CohereChatRequest.SAFETY_MODE_STRICT,
            prompt_truncation=oci_models.CohereChatRequest.PROMPT_TRUNCATION_OFF,
        )

        chat_details = oci_models.ChatDetails(
            compartment_id=settings.OCI_COMPARTMENT_OCID,
            serving_mode=serving_mode,
            chat_request=chat_request,
        )

        result = self._client.chat(chat_details).data
        chat_response = getattr(result, "chat_response", None)
        if chat_response is not None and getattr(chat_response, "text", None):
            return chat_response.text
        return None

    def _call_oci_generic(self, oci_models, question, retrieved_chunks, serving_mode):
        """Rama genérica: Meta Llama, Google Gemini, xAI Grok, etc. en OCI.
        Estos modelos no soportan el parámetro 'documents' con citación
        automática como Cohere, así que el contexto va inyectado directo en
        el mensaje de usuario (build_user_prompt ya arma ese bloque)."""
        user_prompt = build_user_prompt(question, retrieved_chunks)

        messages = [
            oci_models.SystemMessage(content=[oci_models.TextContent(text=SYSTEM_PROMPT)]),
            oci_models.UserMessage(content=[oci_models.TextContent(text=user_prompt)]),
        ]

        chat_request = oci_models.GenericChatRequest(
            api_format=oci_models.BaseChatRequest.API_FORMAT_GENERIC,
            messages=messages,
            max_tokens=800,
            temperature=settings.LLM_TEMPERATURE,
        )

        chat_details = oci_models.ChatDetails(
            compartment_id=settings.OCI_COMPARTMENT_OCID,
            serving_mode=serving_mode,
            chat_request=chat_request,
        )

        result = self._client.chat(chat_details).data
        chat_response = getattr(result, "chat_response", None)
        choices = getattr(chat_response, "choices", None) if chat_response else None
        if choices:
            content = choices[0].message.content
            if content:
                return content[0].text
        return None

    def generate_answer(self, question: str, retrieved_chunks: list[dict]) -> str:
        """
        Genera la respuesta final. Si `retrieved_chunks` viene vacío
        (por umbral de score no alcanzado), activa el fallback directamente
        sin siquiera llamar al LLM, para ahorrar costo y evitar alucinaciones.
        """
        if not retrieved_chunks:
            return (
                "No encontré esta información en los documentos disponibles. "
                "Te recomiendo contactar al área correspondiente de Andina Bank "
                "a través de los canales oficiales de soporte."
            )

        if self.provider == "oci" and self._client and settings.OCI_COMPARTMENT_OCID:
            try:
                from oci.generative_ai_inference import models as oci_models

                serving_mode = self._build_serving_mode(oci_models)
                model_id = settings.OCI_GENAI_CHAT_MODEL_ID or ""

                if model_id.startswith("cohere."):
                    text = self._call_oci_cohere(oci_models, question, retrieved_chunks, serving_mode)
                else:
                    text = self._call_oci_generic(oci_models, question, retrieved_chunks, serving_mode)

                if text:
                    return text
            except Exception as exc:
                # Si la integración OCI falla, lo dejamos visible en consola para
                # poder depurar (antes se tragaba el error en silencio).
                print(f"  ⚠️  Error al generar respuesta con OCI Generative AI: {exc}")

            return (
                "No encontré esta información en los documentos disponibles. "
                "Revisa que la configuración de OCI Generative AI esté completa antes de volver a intentar."
            )

        if self.provider == "openai":
            user_prompt = build_user_prompt(question, retrieved_chunks)
            response = self._client.chat.completions.create(
                model=settings.LLM_MODEL_NAME,
                temperature=settings.LLM_TEMPERATURE,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return response.choices[0].message.content

        raise NotImplementedError(f"Proveedor de LLM no soportado aún: {self.provider}")
