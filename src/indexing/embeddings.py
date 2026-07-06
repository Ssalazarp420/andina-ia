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
        if self.provider == "openai":
            from openai import OpenAI

            return OpenAI(api_key=settings.EMBEDDING_API_KEY)

        raise NotImplementedError(f"Proveedor de embeddings no soportado aún: {self.provider}")

    def embed_text(self, text: str) -> list[float]:
        """Genera el vector de embedding para un único texto."""
        if self.provider == "openai":
            response = self._client.embeddings.create(model=self.model_name, input=text)
            return response.data[0].embedding

        raise NotImplementedError(f"Proveedor de embeddings no soportado aún: {self.provider}")

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Genera embeddings para un lote de textos (más eficiente que uno a uno)."""
        if self.provider == "openai":
            response = self._client.embeddings.create(model=self.model_name, input=texts)
            return [item.embedding for item in response.data]

        raise NotImplementedError(f"Proveedor de embeddings no soportado aún: {self.provider}")
