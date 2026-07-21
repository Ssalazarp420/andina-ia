"""
Fase 4 - Reranker.
Reevalúa la relación contextual profunda entre la pregunta y cada
fragmento candidato, para reordenar por relevancia real (no solo distancia vectorial).
"""

from src.config import settings


class Reranker:
    def __init__(self, provider: str | None = None):
        self.provider = provider or settings.RERANKER_PROVIDER
        self._client = self._init_client()

    def _init_client(self):
        if self.provider == "cohere":
            if settings.RERANKER_API_KEY:
                try:
                    from cohere import Client

                    return Client(api_key=settings.RERANKER_API_KEY)
                except Exception as exc:
                    print(f"  ⚠️  No se pudo inicializar el cliente Cohere externo (rerank): {exc}")

            try:
                import oci
                from oci.retry import NoneRetryStrategy

                if not settings.OCI_COMPARTMENT_OCID:
                    return None

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
                print(f"  ⚠️  No se pudo inicializar el cliente OCI Generative AI (rerank): {exc}")
                return None

        return None

    @staticmethod
    def _build_serving_mode(oci_models_module):
        from src.config import settings

        if settings.OCI_GENAI_RERANK_ENDPOINT_ID:
            return oci_models_module.DedicatedServingMode(endpoint_id=settings.OCI_GENAI_RERANK_ENDPOINT_ID)

        return oci_models_module.OnDemandServingMode(model_id=settings.OCI_GENAI_RERANK_MODEL_ID)

    def rerank(self, question: str, candidates: list[dict], top_n: int = 5) -> list[dict]:
        """
        Recibe los candidatos crudos de la búsqueda vectorial y devuelve
        el top_n final reordenado, cada uno con un campo 'score' normalizado (0-1).
        """
        if not candidates:
            return []

        if self.provider == "cohere" and self._client:
            if settings.RERANKER_API_KEY:
                try:
                    response = self._client.rerank(
                        model=settings.RERANKER_MODEL_NAME or "rerank-v3.5",
                        query=question,
                        documents=[candidate.get("text", "") for candidate in candidates],
                        top_n=top_n,
                    )
                    ranked_candidates = []
                    for result in response.results:
                        index = result.index
                        if 0 <= index < len(candidates):
                            ranked_candidates.append(
                                {
                                    **candidates[index],
                                    "score": float(result.relevance_score),
                                }
                            )
                    if ranked_candidates:
                        return ranked_candidates[:top_n]
                except Exception as exc:
                    print(f"  ⚠️  Rerank externo no disponible, usando fallback local: {exc}")

            if settings.OCI_COMPARTMENT_OCID:
                try:
                    from oci.generative_ai_inference import models as oci_models

                    serving_mode = self._build_serving_mode(oci_models)

                    rerank_request = oci_models.RerankTextDetails(
                        compartment_id=settings.OCI_COMPARTMENT_OCID,
                        input=question,
                        documents=[candidate.get("text", "") for candidate in candidates],
                        top_n=top_n,
                        serving_mode=serving_mode,
                        is_echo=False,
                    )

                    result = self._client.rerank_text(rerank_request).data
                    ranked_candidates = []

                    for document_rank in result.document_ranks:
                        index = document_rank.index
                        if 0 <= index < len(candidates):
                            ranked_candidates.append(
                                {
                                    **candidates[index],
                                    "score": float(document_rank.relevance_score),
                                }
                            )

                    if ranked_candidates:
                        return ranked_candidates[:top_n]
                except Exception as exc:
                    print(f"  ⚠️  Rerank OCI no disponible, usando fallback local: {exc}")

        # Fallback local por distancia vectorial. Chroma se configura con
        # métrica coseno (ver VectorStore), así que 'distance' está en el
        # rango aproximado [0, 2] y este score queda razonablemente acotado.
        scored = []
        for candidate in candidates:
            distance = candidate.get("distance", 1.0)
            provisional_score = max(0.0, 1.0 - distance)
            scored.append({**candidate, "score": provisional_score})

        scored.sort(key=lambda c: c["score"], reverse=True)
        return scored[:top_n]
