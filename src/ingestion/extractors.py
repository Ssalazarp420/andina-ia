"""
Fase 2 - Extracción por formato.
Cada función recibe la ruta de un archivo y devuelve texto crudo (sin limpiar).
El manejo de errores es obligatorio: un archivo corrupto NO debe tumbar el pipeline completo.
"""

from pathlib import Path


class ExtractionError(Exception):
    """Error controlado al extraer contenido de un documento."""


def extract_pdf(file_path: str) -> str:
    """
    Extrae texto de un PDF. Si el PDF es escaneado (imagen), debe
    hacer fallback a OCR (pendiente: integrar pytesseract / OCR de OCI Vision).
    """
    try:
        import pdfplumber

        text_chunks = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text_chunks.append(page_text)

        full_text = "\n".join(text_chunks).strip()

        if not full_text:
            # TODO: Fase 2 - fallback a OCR cuando el PDF es una imagen escaneada
            raise ExtractionError(
                f"'{file_path}' no devolvió texto extraíble. Posible PDF escaneado: requiere OCR."
            )

        return full_text

    except Exception as exc:
        raise ExtractionError(f"Fallo al extraer PDF '{file_path}': {exc}") from exc


def extract_docx(file_path: str) -> str:
    """Extrae texto de un Word, preservando títulos/párrafos en orden."""
    try:
        import docx

        document = docx.Document(file_path)
        return "\n".join(p.text for p in document.paragraphs if p.text.strip())
    except Exception as exc:
        raise ExtractionError(f"Fallo al extraer DOCX '{file_path}': {exc}") from exc


def extract_xlsx(file_path: str) -> str:
    """
    Convierte cada fila en una frase estructurada, repitiendo encabezados
    de columna (según la estrategia definida en Fase 2 para datos tabulares).
    """
    try:
        import pandas as pd

        sheets = pd.read_excel(file_path, sheet_name=None)
        rows_as_text = []

        for sheet_name, df in sheets.items():
            for _, row in df.iterrows():
                row_text = ", ".join(f"{col}: {row[col]}" for col in df.columns)
                rows_as_text.append(f"[Hoja: {sheet_name}] {row_text}")

        return "\n".join(rows_as_text)
    except Exception as exc:
        raise ExtractionError(f"Fallo al extraer XLSX '{file_path}': {exc}") from exc


def extract_csv(file_path: str) -> str:
    """Misma lógica que XLSX pero para CSV."""
    try:
        import pandas as pd

        df = pd.read_csv(file_path)
        rows_as_text = [
            ", ".join(f"{col}: {row[col]}" for col in df.columns)
            for _, row in df.iterrows()
        ]
        return "\n".join(rows_as_text)
    except Exception as exc:
        raise ExtractionError(f"Fallo al extraer CSV '{file_path}': {exc}") from exc


def extract_pptx(file_path: str) -> str:
    """Extrae texto de cada slide, incluyendo notas del orador."""
    try:
        from pptx import Presentation

        prs = Presentation(file_path)
        slides_text = []

        for i, slide in enumerate(prs.slides, start=1):
            slide_text = []
            for shape in slide.shapes:
                if shape.has_text_frame:
                    slide_text.append(shape.text_frame.text)

            notes = ""
            if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
                notes = slide.notes_slide.notes_text_frame.text

            combined = "\n".join(slide_text)
            slides_text.append(f"[Slide {i}] {combined}\n[Notas] {notes}")

        return "\n\n".join(slides_text)
    except Exception as exc:
        raise ExtractionError(f"Fallo al extraer PPTX '{file_path}': {exc}") from exc


def extract_markdown_or_html(file_path: str) -> str:
    """Limpia marcas de Markdown/HTML manteniendo el contenido legible."""
    try:
        from bs4 import BeautifulSoup

        raw = Path(file_path).read_text(encoding="utf-8", errors="ignore")

        if file_path.lower().endswith((".html", ".htm")):
            return BeautifulSoup(raw, "html.parser").get_text(separator="\n").strip()

        return raw  # Markdown se limpia con más detalle en cleaning.py
    except Exception as exc:
        raise ExtractionError(f"Fallo al extraer Markdown/HTML '{file_path}': {exc}") from exc


EXTRACTOR_BY_EXTENSION = {
    ".pdf": extract_pdf,
    ".docx": extract_docx,
    ".xlsx": extract_xlsx,
    ".csv": extract_csv,
    ".pptx": extract_pptx,
    ".md": extract_markdown_or_html,
    ".html": extract_markdown_or_html,
    ".htm": extract_markdown_or_html,
}


def extract_document(file_path: str) -> str:
    """Router principal: elige el extractor correcto según la extensión del archivo."""
    extension = Path(file_path).suffix.lower()
    extractor = EXTRACTOR_BY_EXTENSION.get(extension)

    if extractor is None:
        raise ExtractionError(f"Formato no soportado: '{extension}' ({file_path})")

    return extractor(file_path)
