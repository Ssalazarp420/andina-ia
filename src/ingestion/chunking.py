"""
Fase 2 - Chunking (división en fragmentos).
Implementa la estrategia de tamaño fijo con overlap. La estrategia de
estructura lógica (por sección/cláusula) se puede añadir por tipo de documento.
"""

from dataclasses import dataclass, field


@dataclass
class Chunk:
    text: str
    metadata: dict = field(default_factory=dict)


def fixed_size_chunking(
    text: str,
    chunk_size: int = 800,
    overlap: int = 150,
) -> list[str]:
    """
    Divide el texto en fragmentos de `chunk_size` caracteres con un
    `overlap` entre fragmentos contiguos para no cortar ideas por la mitad.
    """
    if chunk_size <= overlap:
        raise ValueError("chunk_size debe ser mayor que overlap.")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk_text = text[start:end].strip()

        if chunk_text:
            chunks.append(chunk_text)

        if end == text_length:
            break

        start = end - overlap

    return chunks


def build_chunks_with_metadata(
    text: str,
    base_metadata: dict,
    chunk_size: int = 800,
    overlap: int = 150,
) -> list[Chunk]:
    """
    Aplica el chunking de tamaño fijo y adjunta los metadatos obligatorios
    de la Fase 2: categoría, origen, temporalidad, gobernanza, ubicación.
    `base_metadata` debe incluir al menos: categoria, origen_archivo, empresa_origen.
    """
    raw_chunks = fixed_size_chunking(text, chunk_size=chunk_size, overlap=overlap)

    return [
        Chunk(
            text=chunk_text,
            metadata={
                **base_metadata,
                "chunk_index": i,
                "total_chunks": len(raw_chunks),
            },
        )
        for i, chunk_text in enumerate(raw_chunks)
    ]
