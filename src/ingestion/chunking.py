"""
Fase 2 - Chunking (división en fragmentos).
Implementa tamaño fijo con overlap, aplicado POR SEGMENTO (página, slide,
hoja o sección) en vez de sobre el documento entero. Así cada chunk conserva
la ubicación exacta de origen para la citación de la Fase 5, y nunca se
mezcla contenido de dos páginas/slides distintos en un mismo fragmento.
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
    segments: list[tuple[str, str]],
    base_metadata: dict,
    chunk_size: int = 800,
    overlap: int = 150,
) -> list[Chunk]:
    """
    Aplica el chunking de tamaño fijo a cada segmento (página/slide/hoja/sección)
    por separado y adjunta los metadatos obligatorios de la Fase 2: categoría,
    origen, temporalidad, gobernanza y ubicación exacta (`seccion_origen`).

    `segments` es la lista (etiqueta_de_ubicacion, texto) que devuelve
    `extract_document` ya limpia (post `clean_text`).
    `base_metadata` debe incluir al menos: categoria, origen_archivo, empresa_origen.
    """
    all_chunks: list[Chunk] = []
    global_index = 0

    for seccion_origen, segment_text in segments:
        raw_chunks = fixed_size_chunking(segment_text, chunk_size=chunk_size, overlap=overlap)

        for chunk_text in raw_chunks:
            all_chunks.append(
                Chunk(
                    text=chunk_text,
                    metadata={
                        **base_metadata,
                        "seccion_origen": seccion_origen,
                        "chunk_index": global_index,
                    },
                )
            )
            global_index += 1

    # total_chunks solo se conoce al final, se completa en una segunda pasada.
    for chunk in all_chunks:
        chunk.metadata["total_chunks"] = len(all_chunks)

    return all_chunks