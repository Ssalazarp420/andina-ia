"""
Fase 5 - Generación de la respuesta final (inferencia del LLM).
"""

from src.config import settings
from src.generation.prompts import SYSTEM_PROMPT, build_user_prompt


class ResponseGenerator:
    def __init__(self, provider: str | None = None):
        self.provider = provider or settings.LLM_PROVIDER
        self._client = self._init_client()

    def _init_client(self):
        if self.provider == "openai":
            from openai import OpenAI

            return OpenAI(api_key=settings.LLM_API_KEY)

        raise NotImplementedError(f"Proveedor de LLM no soportado aún: {self.provider}")

    def generate_answer(self, question: str, retrieved_chunks: list[dict]) -> str:
        """
        Genera la respuesta final. Si `retrieved_chunks` viene vacío
        (por umbral de score no alcanzado), activa el fallback directamente
        sin siquiera llamar al LLM, para ahorrar costo y evitar alucinaciones.
        """
        if not retrieved_chunks:
            return (
                "No encontré esta información en los documentos disponibles. "
                "Te recomiendo contactar al área correspondiente de Andina Bank "
                "a través de los canales oficiales de soporte."
            )

        user_prompt = build_user_prompt(question, retrieved_chunks)

        if self.provider == "openai":
            response = self._client.chat.completions.create(
                model=settings.LLM_MODEL_NAME,
                temperature=settings.LLM_TEMPERATURE,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return response.choices[0].message.content

        raise NotImplementedError(f"Proveedor de LLM no soportado aún: {self.provider}")
