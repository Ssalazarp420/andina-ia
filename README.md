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
| Embeddings | _(definir modelo)_ |
| Base vectorial | Chroma (local) → Oracle AI Vector Search (producción) |
| Reranker | _(definir proveedor)_ |
| LLM | _(definir proveedor)_ |
| Interfaz | Streamlit |
| Nube | Oracle Cloud Infrastructure (OCI) |

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
# Editar .env con tus API keys

# 5. Ejecutar ingesta inicial (Fases 2 y 3)
python scripts/run_ingestion.py

# 6. Levantar la interfaz
streamlit run app/streamlit_app.py
```

## 🧪 Casos de Prueba (QA)
_(Completar con ejemplos reales una vez cargados los documentos de Andina Bank)_

| # | Pregunta del colaborador | Respuesta del agente | Fuente citada |
|---|---|---|---|
| 1 | _Ej: ¿Cuál es la política de reembolso de transacciones no reconocidas?_ | _(pendiente)_ | _(pendiente)_ |
| 2 | | | |

## ☁️ Evidencia de Deploy en OCI
_(Completar con URL pública y/o capturas de pantalla)_

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
- [ ] Fase 1: Documentos de prueba de Andina Bank (Fintech)
- [ ] Fase 2: Extracción y chunking
- [ ] Fase 3: Indexación vectorial
- [ ] Fase 4: Retrieval + Reranker
- [ ] Fase 5: Generación y control de alucinaciones
- [ ] Fase 6: Interfaz Streamlit
- [ ] Fase 7: Deploy en OCI
- [ ] Fase 8: Logging y evidencias

---

*Proyecto ficticio con fines educativos — Challenge Alura Agentes.*
