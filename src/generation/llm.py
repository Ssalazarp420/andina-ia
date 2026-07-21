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
        if self.provider == "cohere":
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

        user_prompt = build_user_prompt(question, retrieved_chunks)

        if self.provider == "cohere" and self._client and settings.OCI_COMPARTMENT_OCID:
            try:
                from oci.generative_ai_inference import models as oci_models

                serving_mode = self._build_serving_mode(oci_models)
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

                # IMPORTANTE: el SDK de OCI espera un ChatDetails como top-level
                # request, con compartment_id + serving_mode a ese nivel (no
                # dentro del CohereChatRequest). Pasar el CohereChatRequest
                # directo a .chat() es inválido y siempre falla.
                chat_details = oci_models.ChatDetails(
                    compartment_id=settings.OCI_COMPARTMENT_OCID,
                    serving_mode=serving_mode,
                    chat_request=chat_request,
                )

                result = self._client.chat(chat_details).data
                chat_response = getattr(result, "chat_response", None)
                if chat_response is not None and getattr(chat_response, "text", None):
                    return chat_response.text
            except Exception as exc:
                # Si la integración OCI falla, lo dejamos visible en consola para
                # poder depurar (antes se tragaba el error en silencio).
                print(f"  ⚠️  Error al generar respuesta con OCI Cohere: {exc}")

            return (
                "No encontré esta información en los documentos disponibles. "
                "Revisa que la configuración de OCI Cohere esté completa antes de volver a intentar."
            )

        if self.provider == "openai":
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
