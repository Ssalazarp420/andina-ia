"""
Fase 2 - Limpieza del texto extraído.
Elimina ruidos que no aportan significado semántico antes del chunking.
"""

import re


def clean_text(raw_text: str) -> str:
    """Aplica una serie de reglas de limpieza sobre el texto crudo."""
    text = raw_text

    # Espacios y saltos de línea duplicados
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)

    # Numeración de páginas sueltas (ej: "Página 3", "3 / 20")
    text = re.sub(r"(?im)^\s*p[aá]gina\s+\d+(\s+de\s+\d+)?\s*$", "", text)
    text = re.sub(r"(?m)^\s*\d+\s*/\s*\d+\s*$", "", text)

    # Caracteres de control / formato oculto
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)

    # Marcas residuales de Markdown simples (#, *, _) si vienen de un .md
    text = re.sub(r"(?m)^#{1,6}\s*", "", text)

    return text.strip()


def remove_repeated_headers_footers(pages: list[str]) -> list[str]:
    """
    Detecta líneas que se repiten idénticas en la mayoría de las páginas
    (encabezados/pies de página) y las elimina.
    Recibe una lista de textos, uno por página.
    """
    if len(pages) < 3:
        return pages

    line_counts: dict[str, int] = {}
    for page in pages:
        for line in set(line.strip() for line in page.splitlines() if line.strip()):
            line_counts[line] = line_counts.get(line, 0) + 1

    threshold = max(2, int(len(pages) * 0.6))
    repeated_lines = {line for line, count in line_counts.items() if count >= threshold}

    cleaned_pages = []
    for page in pages:
        kept_lines = [line for line in page.splitlines() if line.strip() not in repeated_lines]
        cleaned_pages.append("\n".join(kept_lines))

    return cleaned_pages
