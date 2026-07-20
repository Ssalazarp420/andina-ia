"""
Configuración centralizada de Andina IA.
Carga las variables de entorno una sola vez y las expone como constantes
para el resto de los módulos (ingestion, indexing, retrieval, generation).
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # --- App ---
    APP_NAME: str = os.getenv("APP_NAME", "Andina IA")
    APP_ENV: str = os.getenv("APP_ENV", "local")

    # --- LLM (Fase 5) ---
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "cohere")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", 0.1))

    # --- Embeddings (Fase 3) ---
    EMBEDDING_PROVIDER: str = os.getenv("EMBEDDING_PROVIDER", "cohere")
    EMBEDDING_API_KEY: str = os.getenv("EMBEDDING_API_KEY", "")
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "")

    # --- Vector DB (Fase 3) ---
    VECTOR_DB_PROVIDER: str = os.getenv("VECTOR_DB_PROVIDER", "chroma")
    VECTOR_DB_COLLECTION_NAME: str = os.getenv("VECTOR_DB_COLLECTION_NAME", "andina_bank_kb")

    # --- Retrieval / Reranker (Fase 4) ---
    RETRIEVAL_TOP_K: int = int(os.getenv("RETRIEVAL_TOP_K", 20))
    RERANK_TOP_N: int = int(os.getenv("RERANK_TOP_N", 5))
    SCORE_THRESHOLD: float = float(os.getenv("SCORE_THRESHOLD", 0.55))
    RERANKER_PROVIDER: str = os.getenv("RERANKER_PROVIDER", "cohere")
    RERANKER_MODEL_NAME: str = os.getenv("RERANKER_MODEL_NAME", "")

    # --- OCI (Fase 7) ---
    OCI_CONFIG_FILE: str = os.getenv("OCI_CONFIG_FILE", os.path.expanduser("~/.oci/config"))
    OCI_CONFIG_PROFILE: str = os.getenv("OCI_CONFIG_PROFILE", "DEFAULT")
    OCI_REGION: str = os.getenv("OCI_REGION", "sa-saopaulo-1")
    OCI_COMPARTMENT_OCID: str = os.getenv("OCI_COMPARTMENT_OCID", "")
    OCI_OBJECT_STORAGE_BUCKET: str = os.getenv("OCI_OBJECT_STORAGE_BUCKET", "andina-bank-documentos")
    OCI_VAULT_OCID: str = os.getenv("OCI_VAULT_OCID", "")
    OCI_GENAI_EMBED_MODEL_ID: str = os.getenv("OCI_GENAI_EMBED_MODEL_ID", "")
    OCI_GENAI_EMBED_ENDPOINT_ID: str = os.getenv("OCI_GENAI_EMBED_ENDPOINT_ID", "")
    OCI_GENAI_CHAT_MODEL_ID: str = os.getenv("OCI_GENAI_CHAT_MODEL_ID", "")
    OCI_GENAI_CHAT_ENDPOINT_ID: str = os.getenv("OCI_GENAI_CHAT_ENDPOINT_ID", "")
    OCI_GENAI_RERANK_MODEL_ID: str = os.getenv("OCI_GENAI_RERANK_MODEL_ID", "")
    OCI_GENAI_RERANK_ENDPOINT_ID: str = os.getenv("OCI_GENAI_RERANK_ENDPOINT_ID", "")

    # --- Logging (Fase 8) ---
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "jsonl")


settings = Settings()
