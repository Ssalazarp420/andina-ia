# 🏦 Andina IA — Agente Corporativo RAG para Andina Bank

> Agente de Inteligencia Artificial que responde preguntas de los colaboradores de **Andina Bank** (fintech ficticia) basándose únicamente en su documentación interna oficial, con citación de fuentes y trazabilidad completa.

Proyecto desarrollado para el **Challenge Alura Agentes**.

---

## 📌 Descripción General
Los colaboradores de Andina Bank pierden tiempo buscando información dispersa en políticas internas, manuales, tablas de tarifas y preguntas frecuentes. **Andina IA** centraliza esa base documental en un agente conversacional que responde en lenguaje natural, citando siempre el documento y la ubicación exacta (página, hoja o sección) de donde proviene cada dato, y que declara explícitamente cuando no tiene información suficiente en vez de inventar una respuesta.

## 🏗️ Arquitectura de la Solución
```
Documentos (PDF/CSV/XLSX)
        │
        ▼
[Fase 2] Extracción por página/hoja/slide + limpieza + chunking ──► [Fase 3] Embeddings (Cohere Embed v4) ──► Chroma
        │                                                                                                          │
        └──────────────────────────────────────────────► [Fase 4] Retrieval (top-20) + Reranker (top-5) ◄─────────┘
                                                                        │
                                                                        ▼
                                                    [Fase 5] Generación LLM (mundo cerrado, Gemini 2.5 Flash-Lite)
                                                                        │
                                                                        ▼
                                                    [Fase 6] Interfaz (Streamlit) + Feedback
                                                                        │
                                                                        ▼
                                        [Fase 7] Deploy en OCI (Container Instance, ARM) + [Fase 8] Logging JSONL
```

Cada chunk conserva metadatos de origen (`empresa_origen`, `categoria`, `origen_archivo`, `formato_archivo`, `seccion_origen`) desde la extracción, lo que permite que la Fase 5 cite la ubicación exacta del fragmento (ej. "Página 3", "Hoja: Tarifas", "Diapositiva 5") en cada respuesta.

## 🛠️ Stack Tecnológico
| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.11+ |
| Orquestación | LangChain |
| Extracción | pypdf, pdfplumber, pandas, python-docx, python-pptx, beautifulsoup4 |
| Embeddings | OCI Generative AI Inference — Cohere `embed-v4.0` (on-demand) |
| Base vectorial | Chroma (local, persistente, métrica coseno) |
| Reranker | Cohere API externa (`rerank-multilingual-v3.0`), con fallback local por distancia vectorial |
| LLM | OCI Generative AI Inference — Google `gemini-2.5-flash-lite` (on-demand) |
| Interfaz | Streamlit (chat, historial, feedback 👍/👎, fuentes citadas) |
| Contenerización | Docker (multi-arch: build ARM64 para OCI) |
| Nube | Oracle Cloud Infrastructure (OCI) — OCIR, Container Instances, Vault, VCN, IAM |
| Logging | JSON Lines (`.jsonl`) — pregunta, fuentes recuperadas, respuesta, latencia |

## 🔀 Reranker y estrategia de fallback
La capa de recuperación usa un reranker para reordenar por relevancia real los fragmentos que trae la búsqueda vectorial, antes de armar el contexto final (Fase 4).

Se implementó en cascada, de mayor a menor precisión:

1. **Cohere API externa** (`rerank-multilingual-v3.0`, vía API key propia de Cohere) — es la opción activa hoy y la que efectivamente reordena los resultados con mejor precisión.
2. **OCI Generative AI (Cohere Rerank)** — Oracle solo ofrece los modelos de Rerank en modo *dedicated* (clusters con costo fijo), no on-demand. En una cuenta free tier esta rama devuelve 404 y nunca llega a usarse; se deja implementada para cuando el proyecto migre a un cluster dedicado.
3. **Fallback local por distancia vectorial** — si ninguna de las dos anteriores está disponible, se ordena por la distancia coseno que ya devuelve Chroma. Es la red de seguridad que garantiza que la app nunca se caiga por falta de un reranker externo.

> Nota de diseño: se usan tres proveedores de IA distintos en este proyecto (OCI Cohere para embeddings, OCI Google Gemini para el LLM, y Cohere externo para el reranker) porque en la región/tenancy usada no todos los modelos de un mismo proveedor están disponibles en modo on-demand para todas las tareas. Queda documentado como decisión consciente, no como una limitación oculta.

## 🚀 Guía de Despliegue Local
```bash
# 1. Clonar el repositorio
git clone https://github.com/Ssalazarp420/andina-ia.git
cd andina-ia

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys (LLM_MODEL_NAME, EMBEDDING_MODEL_NAME,
# OCI_COMPARTMENT_OCID, RERANKER_API_KEY, etc.)

# 5. Ejecutar ingesta inicial (Fases 2 y 3)
python scripts/run_ingestion.py

# 6. Levantar la interfaz
streamlit run app/streamlit_app.py
```

### Ejecución con Docker (equivalente al entorno de producción en OCI)
```bash
docker build -t andina-ia:latest -f docker/Dockerfile .

docker run --rm -p 8501:8501 --env-file .env \
  -v ~/.oci:/root/.oci \
  -e OCI_CONFIG_FILE=/root/.oci/config \
  andina-ia:latest
```

## 🧪 Casos de Prueba (QA)
| # | Pregunta del colaborador | Respuesta del agente | Fuente citada |
|---|---|---|---|
| 1 | ¿Cuál es el límite mensual de la Cuenta Andina Plus? | El límite mensual de transferencias para la Cuenta Andina Plus es de $80.000.000 COP. | `Preguntas_Frecuentes_Transacciones_Transferencias_y_Limites.pdf`, Página 1; `limites_y_tarifas_por_producto.csv`, Tabla completa |
| 2 | _(agregar)_ | | |
| 3 | _(agregar)_ | | |

> 💡 Sugerencia: agregá 2-3 preguntas más antes de la entrega, probadas directamente sobre la app en OCI (no en local), para que el README refleje el comportamiento real en producción. Buenos candidatos: una pregunta sobre comisiones, una sobre prevención de fraude, y una pregunta *fuera* del alcance de los documentos, para mostrar el fallback ("No encontré esta información...").

## ☁️ Evidencia de Deploy en OCI

**Servicios de OCI utilizados:** OCI Container Registry (OCIR), OCI Container Instances (shape `CI.Standard.A1.Flex`, ARM), OCI Vault, OCI VCN, OCI IAM (Dynamic Groups + Políticas), OCI Generative AI Inference.

**Acceso en vivo:** `http://<IP_PUBLICA>:8501` _(reemplazar con la IP pública del Container Instance activo al momento de la evaluación — recordar que puede cambiar si se recrea la instancia)_

**Evidencia multimedia:**

_(Insertar acá las capturas de pantalla: 1) consola de OCI con el Container Instance en estado `ACTIVE`, 2) navegador con la app respondiendo la pregunta de prueba desde la IP pública)_

```markdown
![Container Instance activo en OCI](docs/evidencia/container-instance-active.png)
![Agente respondiendo desde la nube](docs/evidencia/respuesta-en-vivo.png)
```

## 📝 Registro de Ejecución (Fase 8)
Cada interacción con el agente se registra en formato **JSON Lines** (`src/utils/logger.py`), capturando pregunta, fuentes recuperadas (documento + score), respuesta generada y latencia:

```json
{"timestamp": 1784588878.77, "app": "Andina IA", "env": "production", "question": "¿cuál es el límite mensual de la Cuenta Andina Plus?", "retrieved_sources": [{"origen_archivo": "Preguntas_Frecuentes_Transacciones_Transferencias_y_Limites.pdf", "score": 0.91}, {"origen_archivo": "limites_y_tarifas_por_producto.csv", "score": 0.87}], "answer": "El límite mensual de transferencias...", "latency_ms": 4023.7}
```

- **Local:** los logs se escriben en `logs/andina_ia_interactions.jsonl`.
- **En OCI:** el Container Instance escribe estos mismos logs dentro de su filesystem interno (`env: "production"`, según la variable `APP_ENV`). Al ser un filesystem efímero, **los registros no persisten si el contenedor se recrea o reinicia** — limitación conocida y aceptada para el alcance de este challenge. La evolución natural sería redirigir la salida a OCI Logging para retención centralizada (fuera del alcance de esta entrega).
- **Trazabilidad:** cada línea permite reconstruir qué preguntó el colaborador, qué documentos se usaron como contexto, con qué score de relevancia, y qué respondió el modelo, cumpliendo el requisito central de auditoría de extremo a extremo de la Fase 8.
- **Limitación conocida:** el log actual guarda el nombre del documento y el score de cada fuente recuperada, pero no el texto exacto del fragmento (`seccion_origen` ni el contenido del chunk) que se inyectó en el prompt. Para una auditoría completa "pregunta → contexto exacto → respuesta" sería necesario ampliar `log_interaction()` para incluir también `seccion_origen` y el texto del chunk. Se documenta como mejora futura, no bloqueante para la entrega actual.

---

## 📂 Estructura del Repositorio
```
andina-ia/
├── app/                # Interfaz Streamlit (Fase 6)
├── data/
│   ├── raw/            # Documentos originales de Andina Bank (no versionados)
│   └── processed/      # Chunks procesados (no versionados)
├── docker/             # Dockerfile para OCIR/OKE (Fase 7)
├── docs/evidencia/      # Capturas/videos del deploy en OCI
├── infra/oci/          # Notas y scripts de infraestructura OCI (Fase 7)
├── logs/               # Logs locales .jsonl (Fase 8)
├── scripts/            # Scripts ejecutables (ingesta, etc.)
├── src/
│   ├── ingestion/      # Extracción, limpieza y chunking (Fase 2)
│   ├── indexing/       # Embeddings y base vectorial (Fase 3)
│   ├── retrieval/      # Búsqueda + Reranker (Fase 4)
│   ├── generation/     # Prompts y llamado al LLM (Fase 5)
│   └── utils/          # Config y logging compartido
├── tests/              # Pruebas unitarias
├── .env.example
├── requirements.txt
└── README.md
```

## 📋 Estado del Proyecto (Kanban)
- [x] Fase 1: Documentos de prueba de Andina Bank (Fintech)
- [x] Fase 2: Extracción y chunking (por página/hoja/slide, con `seccion_origen`)
- [x] Fase 3: Indexación vectorial (Cohere Embed v4)
- [x] Fase 4: Retrieval + Reranker
- [x] Fase 5: Generación y control de alucinaciones
- [x] Fase 6: Interfaz Streamlit
- [x] Fase 7: Deploy en OCI (Container Instance ARM, activo)
- [x] Fase 8: Logging y evidencias

---

*Proyecto ficticio con fines educativos — Challenge Alura Agentes.*