"""
Fase 3 - Almacenamiento e indexación vectorial.
Implementación local con Chroma para desarrollo. En producción (Fase 7),
este módulo se reemplaza/extiende para apuntar a Oracle AI Vector Search.
"""

from src.config import settings
from src.ingestion.chunking import Chunk


class VectorStore:
    def __init__(self, collection_name: str | None = None):
        self.collection_name = collection_name or settings.VECTOR_DB_COLLECTION_NAME
        self._client = self._init_client()
        self._collection = self._client.get_or_create_collection(self.collection_name)

    def _init_client(self):
        if settings.VECTOR_DB_PROVIDER == "chroma":
            import chromadb

            return chromadb.PersistentClient(path="./vector_store")

        # TODO: Fase 7 - agregar rama para Oracle AI Vector Search / Qdrant / Pinecone
        raise NotImplementedError(
            f"Proveedor de base vectorial no soportado aún: {settings.VECTOR_DB_PROVIDER}"
        )

    def add_chunks(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        """Inserta chunks + sus embeddings + metadatos en la base vectorial."""
        ids = [f"{c.metadata.get('origen_archivo', 'doc')}_{c.metadata.get('chunk_index', i)}" for i, c in enumerate(chunks)]

        self._collection.add(
            ids=ids,
            documents=[c.text for c in chunks],
            embeddings=embeddings,
            metadatas=[c.metadata for c in chunks],
        )

    def query(self, query_embedding: list[float], top_k: int = 20, where: dict | None = None):
        """Búsqueda semántica preliminar, con filtrado opcional por metadatos (Fase 4)."""
        return self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
        )
