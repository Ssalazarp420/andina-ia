"""
Fase 5 - Plantillas de prompt.
Principio de "mundo cerrado": el LLM responde ÚNICAMENTE con el contexto provisto.
"""

SYSTEM_PROMPT = """\
Eres Andina IA, el asistente virtual interno de Andina Bank.

REGLAS ESTRICTAS:
1. Responde ÚNICAMENTE utilizando la información contenida en el "CONTEXTO" provisto.
2. Si el contexto no contiene la información necesaria para responder con certeza,
   responde exactamente: "No encontré esta información en los documentos disponibles."
   y sugiere el canal oficial correspondiente si está disponible en el contexto.
3. Nunca inventes datos, cifras, políticas ni nombres que no figuren en el contexto.
4. Cita siempre la fuente de cada afirmación (nombre del documento y sección/página).
5. Responde en español, de forma clara, ejecutiva y profesional.
"""

USER_PROMPT_TEMPLATE = """\
CONTEXTO:
{context_block}

PREGUNTA DEL COLABORADOR:
{question}

Responde siguiendo estrictamente las reglas del sistema. Al final, incluye
una sección "Fuentes:" listando los documentos y secciones citados.
"""


def build_context_block(retrieved_chunks: list[dict]) -> str:
    """Ensambla el bloque de contexto enriquecido a partir de los chunks ya rerankeados."""
    blocks = []
    for i, chunk in enumerate(retrieved_chunks, start=1):
        meta = chunk.get("metadata", {})
        origen = meta.get("origen_archivo", "documento desconocido")
        seccion = meta.get("seccion_origen", "sección no especificada")
        blocks.append(f"[Fragmento {i} | Fuente: {origen} | {seccion}]\n{chunk['text']}")

    return "\n\n".join(blocks) if blocks else "(Sin fragmentos relevantes encontrados)"


def build_user_prompt(question: str, retrieved_chunks: list[dict]) -> str:
    context_block = build_context_block(retrieved_chunks)
    return USER_PROMPT_TEMPLATE.format(context_block=context_block, question=question)
