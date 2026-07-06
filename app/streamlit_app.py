"""
Fase 6 - Interfaz de chat web para Andina IA.
Ejecutar con: streamlit run app/streamlit_app.py
"""

import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st

from src.retrieval.retriever import Retriever
from src.generation.llm import ResponseGenerator
from src.utils.logger import log_interaction
from src.config import settings

st.set_page_config(page_title=settings.APP_NAME, page_icon="🏦")

st.title(f"🏦 {settings.APP_NAME}")
st.caption(
    "Estás hablando con un agente de Inteligencia Artificial de Andina Bank. "
    "Las respuestas se basan únicamente en documentación interna oficial."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "retriever" not in st.session_state:
    st.session_state.retriever = Retriever()
    st.session_state.generator = ResponseGenerator()

# --- Historial de conversación (persistencia de contexto en la sesión) ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("📎 Fuentes citadas"):
                for src in msg["sources"]:
                    st.write(f"- {src}")

question = st.chat_input("Escribe tu pregunta sobre políticas, productos o procesos de Andina Bank...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Buscando en la documentación oficial..."):
            start_time = time.perf_counter()

            retrieved_chunks = st.session_state.retriever.retrieve_context(question)
            answer = st.session_state.generator.generate_answer(question, retrieved_chunks)

            latency_ms = (time.perf_counter() - start_time) * 1000
            log_interaction(question, retrieved_chunks, answer, latency_ms)

            sources = [
                c.get("metadata", {}).get("origen_archivo", "desconocido")
                for c in retrieved_chunks
            ]

        st.markdown(answer)
        if sources:
            with st.expander("📎 Fuentes citadas"):
                for src in set(sources):
                    st.write(f"- {src}")

        # Módulo de feedback (Fase 6 - requisito obligatorio de interfaz)
        col1, col2 = st.columns(2)
        col1.button("👍", key=f"up_{len(st.session_state.messages)}")
        col2.button("👎", key=f"down_{len(st.session_state.messages)}")

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": list(set(sources))}
    )
