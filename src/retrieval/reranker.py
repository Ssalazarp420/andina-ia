"""
Fase 4 - Reranker.
Reevalúa la relación contextual profunda entre la pregunta y cada
fragmento candidato, para reordenar por relevancia real (no solo distancia vectorial).
"""

from src.config import settings


class Reranker:
    def __init__(self, provider: str | None = None):
        self.provider = provider or settings.RETRIEVAL_TOP_K and "cohere"

    def rerank(self, question: str, candidates: list[dict], top_n: int = 5) -> list[dict]:
        """
        Recibe los candidatos crudos de la búsqueda vectorial y devuelve
        el top_n final reordenado, cada uno con un campo 'score' normalizado (0-1).

        TODO: Fase 4 - integrar modelo real (ej. Cohere Rerank o cross-encoder local)
        Por ahora usa la distancia vectorial invertida como score provisional,
        para no bloquear el desarrollo del resto del pipeline.
        """
        if not candidates:
            return []

        scored = []
        for candidate in candidates:
            distance = candidate.get("distance", 1.0)
            provisional_score = max(0.0, 1.0 - distance)
            scored.append({**candidate, "score": provisional_score})

        scored.sort(key=lambda c: c["score"], reverse=True)
        return scored[:top_n]
