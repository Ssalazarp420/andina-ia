"""
Fase 3 - Generación de embeddings.
IMPORTANTE: el modelo usado aquí debe ser exactamente el mismo que se
use luego en la Fase 4 para vectorizar la pregunta del usuario.
"""

from src.config import settings


class EmbeddingClient:
    """Wrapper simple para desacoplar el proveedor de embeddings del resto del pipeline."""

    def __init__(self, provider: str | None = None, model_name: str | None = None):
        self.provider = provider or settings.EMBEDDING_PROVIDER
        self.model_name = model_name or settings.EMBEDDING_MODEL_NAME
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
                print(f"  ⚠️  No se pudo inicializar el cliente OCI Generative AI (embeddings): {exc}")
                return None

        if self.provider == "openai":
            from openai import OpenAI

            return OpenAI(api_key=settings.EMBEDDING_API_KEY)

        raise NotImplementedError(f"Proveedor de embeddings no soportado aún: {self.provider}")

    def _embed_oci(self, texts: list[str], input_type: str) -> list[list[float]]:
        if not self._client:
            raise RuntimeError("No se pudo inicializar el cliente OCI para embeddings.")

        if not settings.OCI_COMPARTMENT_OCID:
            raise RuntimeError("Falta OCI_COMPARTMENT_OCID para generar embeddings con OCI.")

        if not self.model_name:
            raise RuntimeError("Falta EMBEDDING_MODEL_NAME para generar embeddings con OCI.")

        from oci.generative_ai_inference import models as oci_models

        request = oci_models.EmbedTextDetails(
            compartment_id=settings.OCI_COMPARTMENT_OCID,
            inputs=texts,
            serving_mode=oci_models.OnDemandServingMode(model_id=self.model_name),
            input_type=input_type,
            is_echo=False,
            embedding_types=[oci_models.EmbedTextDetails.EMBEDDING_TYPES_FLOAT],
        )

        result = self._client.embed_text(request).data

        # Los modelos v3 (embed-multilingual-v3.0, etc.) devuelven los vectores
        # directamente en result.embeddings. Cohere Embed v4 (embed-v4.0) en
        # cambio puede devolver result.embeddings == None y traer los vectores
        # dentro de result.embeddings_by_type["float"]. Soportamos ambos casos.
        if result.embeddings:
            return result.embeddings

        embeddings_by_type = getattr(result, "embeddings_by_type", None) or {}
        float_embeddings = embeddings_by_type.get("float")
        if float_embeddings:
            return float_embeddings

        raise RuntimeError(
            "La respuesta de OCI no trajo embeddings en 'embeddings' ni en "
            "'embeddings_by_type[\"float\"]'. Revisa el modelo/parámetros usados."
        )

    def embed_text(self, text: str, input_type: str = "SEARCH_QUERY") -> list[float]:
        """Genera el vector de embedding para un único texto."""
        if self.provider == "cohere":
            embeddings = self._embed_oci([text], input_type=input_type)
            return embeddings[0] if embeddings else []

        if self.provider == "openai":
            if self._client is None:
                raise RuntimeError("No se pudo inicializar el cliente OpenAI para embeddings.")

            response = self._client.embeddings.create(model=self.model_name, input=text)
            return response.data[0].embedding

        raise NotImplementedError(f"Proveedor de embeddings no soportado aún: {self.provider}")

    def embed_batch(self, texts: list[str], input_type: str = "SEARCH_DOCUMENT") -> list[list[float]]:
        """Genera embeddings para un lote de textos (más eficiente que uno a uno)."""
        if self.provider == "cohere":
            return self._embed_oci(texts, input_type=input_type)

        if self.provider == "openai":
            if self._client is None:
                raise RuntimeError("No se pudo inicializar el cliente OpenAI para embeddings.")

            response = self._client.embeddings.create(model=self.model_name, input=texts)
            return [item.embedding for item in response.data]

        raise NotImplementedError(f"Proveedor de embeddings no soportado aún: {self.provider}")
