# 🏦 Andina IA — Agente Corporativo RAG para Andina Bank

> Agente de Inteligencia Artificial que responde preguntas de los colaboradores de **Andina Bank** (fintech ficticia) basándose únicamente en su documentación interna oficial, con citación de fuentes y trazabilidad completa.

Proyecto desarrollado para el **Challenge Alura Agentes**.

---

## 📌 Descripción General
_(Completar en fase de entrega final)_
Resumen ejecutivo del problema de negocio: los colaboradores de Andina Bank pierden tiempo buscando información en políticas, manuales y FAQs dispersos. Andina IA centraliza esa base documental en un agente conversacional confiable.

## 🏗️ Arquitectura de la Solución
```
Documentos (PDF/CSV/XLSX)
        │
        ▼
[Fase 2] Extracción y limpieza ──► [Fase 3] Chunking + Embeddings ──► Base de datos vectorial
        │                                                                     │
        └────────────────────────────► [Fase 4] Retrieval + Reranker ◄───────┘
                                                    │
                                                    ▼
                                    [Fase 5] Generación LLM (mundo cerrado)
                                                    │
                                                    ▼
                                    [Fase 6] Interfaz (Streamlit) + Feedback
                                                    │
                                                    ▼
                                    [Fase 7] Deploy en OCI + [Fase 8] Logging
```

## 🛠️ Stack Tecnológico
| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.11+ |
| Orquestación | LangChain |
| Extracción | pypdf, pdfplumber, pandas, python-docx |
| Embeddings | OCI Generative AI Inference — Cohere `embed-v4.0` (on-demand) |
| Base vectorial | Chroma (local, métrica coseno) → Oracle AI Vector Search (producción) |
| Reranker | Cohere API externa (`rerank-multilingual-v3.0`), con fallback a OCI Cohere Rerank y fallback final por distancia vectorial local |
| LLM | OCI Generative AI Inference — Google `gemini-2.5-flash-lite` (on-demand) |
| Interfaz | Streamlit |
| Nube | Oracle Cloud Infrastructure (OCI) |

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
git clone <URL_DEL_REPO>
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

## 🧪 Casos de Prueba (QA)
| # | Pregunta del colaborador | Respuesta del agente | Fuente citada |
|---|---|---|---|
| 1 | ¿Cuál es el límite mensual de la Cuenta Andina Plus? | El límite mensual de transferencias para la Cuenta Andina Plus es de $80.000.000 COP. | `Cuadro_de_Tarifas_y_Comisiones_del_Servicio.pdf`, `Preguntas_Frecuentes_Transacciones_Transferencias_y_Limites.pdf`, `limites_y_tarifas_por_producto.csv` |
| 2 | _(agregar más ejemplos: cuota de manejo, línea de fraude, transferencias gratis al mes, etc.)_ | | |

## ☁️ Evidencia de Deploy en OCI
_(Completar con URL pública y/o capturas de pantalla — obligatorio para la entrega final)_

---

## 📂 Estructura del Repositorio
```
andina-ia/
├── app/                # Interfaz Streamlit (Fase 6)
├── data/
│   ├── raw/            # Documentos originales de Andina Bank (no versionados)
│   └── processed/      # Chunks procesados (no versionados)
├── docker/             # Dockerfile para OCIR/OKE (Fase 7)
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
- [x] Fase 2: Extracción y chunking
- [x] Fase 3: Indexación vectorial
- [x] Fase 4: Retrieval + Reranker
- [x] Fase 5: Generación y control de alucinaciones
- [x] Fase 6: Interfaz Streamlit
- [ ] Fase 7: Deploy en OCI
- [ ] Fase 8: Logging y evidencias

---

*Proyecto ficticio con fines educativos — Challenge Alura Agentes.*
