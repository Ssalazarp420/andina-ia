"""
Prueba unitaria base para la Fase 2 (chunking).
Ejecutar con: pytest
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.ingestion.chunking import fixed_size_chunking, build_chunks_with_metadata


def test_fixed_size_chunking_respects_overlap():
    text = "a" * 1000
    chunks = fixed_size_chunking(text, chunk_size=300, overlap=50)

    assert len(chunks) > 1
    assert all(len(c) <= 300 for c in chunks)


def test_fixed_size_chunking_raises_on_invalid_params():
    try:
        fixed_size_chunking("texto", chunk_size=100, overlap=200)
        assert False, "Debería haber lanzado ValueError"
    except ValueError:
        pass


def test_build_chunks_with_metadata_includes_base_fields():
    text = "Política de reembolso de Andina Bank. " * 50
    metadata = {"empresa_origen": "Andina Bank", "categoria": "Financiero y Contable"}

    chunks = build_chunks_with_metadata(text, metadata, chunk_size=200, overlap=30)

    assert len(chunks) > 0
    assert chunks[0].metadata["empresa_origen"] == "Andina Bank"
    assert "chunk_index" in chunks[0].metadata
