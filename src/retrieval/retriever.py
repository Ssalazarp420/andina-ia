"""
Fase 4 - Camada de recuperación.
Orquesta: embedding de la pregunta -> búsqueda vectorial amplia ->
filtrado por metadatos -> reranking -> ensamblaje del contexto final.
"""

from src.config import settings
from src.indexing.embeddings import EmbeddingClient
from src.indexing.vector_store import VectorStore
from src.retrieval.reranker import Reranker


class Retriever:
    def __init__(self):
        self.embedding_client = EmbeddingClient()
        self.vector_store = VectorStore()
        self.reranker = Reranker()

    def retrieve_context(
        self,
        question: str,
        metadata_filter: dict | None = None,
        top_k: int = None,
        top_n: int = None,
    ) -> list[dict]:
        """
        Devuelve la lista final de fragmentos (ya reordenados por el reranker)
        con su texto y metadatos, lista para ensamblar el prompt de la Fase 5.
        """
        top_k = top_k or settings.RETRIEVAL_TOP_K
        top_n = top_n or settings.RERANK_TOP_N

        # 1. Embedding de la pregunta
        query_vector = self.embedding_client.embed_text(question, input_type="SEARCH_QUERY")

        # 2. Búsqueda semántica amplia + 3. filtrado por metadatos
        raw_results = self.vector_store.query(
            query_embedding=query_vector,
            top_k=top_k,
            where=metadata_filter,
        )

        candidates = self._format_candidates(raw_results)

        # 4. Reclasificación (Reranking)
        reranked = self.reranker.rerank(question, candidates, top_n=top_n)

        # Umbral de corte semántico (Fase 5 - control de alucinaciones)
        filtered = [c for c in reranked if c["score"] >= settings.SCORE_THRESHOLD]

        return filtered

    @staticmethod
    def _format_candidates(raw_results) -> list[dict]:
        """Normaliza la respuesta cruda de la base vectorial a una lista de dicts."""
        documents = raw_results.get("documents", [[]])[0]
        metadatas = raw_results.get("metadatas", [[]])[0]
        distances = raw_results.get("distances", [[]])[0]

        return [
            {
                "text": doc,
                "metadata": meta,
                "distance": dist,
            }
            for doc, meta, dist in zip(documents, metadatas, distances)
        ]
