"""
Fase 8 - Registro de ejecución.
En local: escribe logs .jsonl. En OCI (Fase 7/8): redirigir stdout a OCI Logging.
"""

import json
import time
from pathlib import Path

from src.config import settings

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "andina_ia_interactions.jsonl"


def log_interaction(
    question: str,
    retrieved_chunks: list[dict],
    answer: str,
    latency_ms: float,
) -> None:
    """Registra cada interacción con trazabilidad completa (pregunta -> contexto -> respuesta)."""
    entry = {
        "timestamp": time.time(),
        "app": settings.APP_NAME,
        "env": settings.APP_ENV,
        "question": question,
        "retrieved_sources": [
            {
                "origen_archivo": c.get("metadata", {}).get("origen_archivo"),
                "score": c.get("score"),
            }
            for c in retrieved_chunks
        ],
        "answer": answer,
        "latency_ms": latency_ms,
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
