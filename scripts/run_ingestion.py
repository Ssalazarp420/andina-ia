"""
Script ejecutable de ingesta completa (Fases 2 y 3).
Recorre data/raw/, extrae, limpia, chunkea, embebe e indexa cada documento.

Uso:
    python scripts/run_ingestion.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.ingestion.extractors import extract_document, ExtractionError
from src.ingestion.cleaning import clean_text
from src.ingestion.chunking import build_chunks_with_metadata
from src.indexing.embeddings import EmbeddingClient
from src.indexing.vector_store import VectorStore

RAW_DATA_DIR = Path("data/raw")

# Metadatos mínimos por categoría de negocio. Ajustar según los documentos reales
# de Andina Bank (ej: "productos", "reglamentos", "seguridad", "tarifas").
CATEGORY_BY_KEYWORD = {
    "reglamento": "Legal y Compliance",
    "privacidad": "Legal y Compliance",
    "tarifa": "Financiero y Contable",
    "comision": "Financiero y Contable",
    "seguridad": "Operacional",
    "fraude": "Operacional",
}


def infer_category(filename: str) -> str:
    lower_name = filename.lower()
    for keyword, category in CATEGORY_BY_KEYWORD.items():
        if keyword in lower_name:
            return category
    return "General"


def run() -> None:
    if not RAW_DATA_DIR.exists() or not any(RAW_DATA_DIR.iterdir()):
        print(f"⚠️  No se encontraron documentos en '{RAW_DATA_DIR}'. Agrega archivos y vuelve a ejecutar.")
        return

    embedding_client = EmbeddingClient()
    vector_store = VectorStore()

    processed_count = 0
    failed_count = 0

    for file_path in RAW_DATA_DIR.iterdir():
        if not file_path.is_file():
            continue

        print(f"Procesando: {file_path.name}")

        try:
            raw_text = extract_document(str(file_path))
        except ExtractionError as e:
            print(f"  ❌ Error de extracción: {e}")
            failed_count += 1
            continue

        cleaned = clean_text(raw_text)

        base_metadata = {
            "empresa_origen": "Andina Bank",
            "origen_archivo": file_path.name,
            "categoria": infer_category(file_path.name),
            "formato_archivo": file_path.suffix.lower(),
        }

        chunks = build_chunks_with_metadata(cleaned, base_metadata)

        if not chunks:
            print("  ⚠️  Documento vacío tras la limpieza, se omite.")
            continue

        embeddings = embedding_client.embed_batch([c.text for c in chunks], input_type="SEARCH_DOCUMENT")
        vector_store.add_chunks(chunks, embeddings)

        print(f"  ✅ {len(chunks)} chunks indexados.")
        processed_count += 1

    print(f"\nResumen: {processed_count} documentos procesados, {failed_count} fallidos.")


if __name__ == "__main__":
    run()
