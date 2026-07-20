# Guía de Desarrollo y Criterios de Entrega: AuraBank Copilot

Este documento establece el alcance oficial, las reglas de negocio y los entregables obligatorios para el proyecto **AuraBank Copilot** en el marco del Challenge Alura Agentes. Actúa como la directriz definitiva en NotebookLM para asegurar que el desarrollo se alinee al 100% con la rúbrica de evaluación.

---

## 1. Identidad y Contexto del Proyecto
*   **Nombre del Sistema:** AuraBank Copilot
*   **Ecosistema Corporativo:** AuraBank (Plataforma Fintech de banca digital y servicios financieros transaccionales).
*   **Propósito:** Un agente de IA corporativo abierto a los colaboradores para resolver dudas sobre los procesos transaccionales, soporte y operaciones del banco.

---

## 2. Componentes Obligatorios del Entregable (Rúbrica Alura)

### A. Repositorio en GitHub
*   Debe ser estrictamente **público**.
*   Debe contar con un historial de commits ordenado que refleje la evolución real del desarrollo.
*   Estructura de carpetas limpia y organizada (ej: `/src`, `/data`, `/docs`).

### B. Base de Conocimiento y Core del Agente
*   El agente inteligente debe ser completamente funcional.
*   **Alcance Documental:** Capaz de responder preguntas precisas basadas en el contenido de la documentación oficial del banco. El pipeline de código debe estar optimizado para leer y procesar archivos en formato **PDF** (Políticas/FAQs generales) y/o **CSV** (Límites transaccionales y tablas de datos planos).

### C. Documentación Técnica (Archivo README.md)
El `README.md` del repositorio de GitHub debe contener obligatoriamente:
1.  **Descripción general:** Qué es AuraBank Copilot y qué problema resuelve en la Fintech.
2.  **Arquitectura de la solución:** Diagrama o flujo lógico del pipeline RAG (ingesta, embeddings, recuperación y generación).
3.  **Stack Tecnológico:** Herramientas utilizadas (ej: Python, LangChain/LangGraph, Streamlit, etc.).
4.  **Guía de despliegue/ejecución:** Instrucciones paso a paso para correr el proyecto de forma local o en la nube.
5.  **Casos de Prueba:** Ejemplos reales de preguntas financieras que el agente puede responder y ejemplos de las respuestas precisas generadas por el modelo.

### D. Evidencia de Despliegue en la Nube (OCI)
*   Demostración de que la aplicación web del agente está corriendo en producción en **Oracle Cloud Infrastructure**.
*   **Soportes válidos:** Inclusión en el README del enlace público activo del agente y/o una captura de pantalla clara de la aplicación web operando desde el entorno en línea de OCI.

---

## 3. Directiva de Trabajo para NotebookLM
*   Diseña el código y los prompts priorizando la lectura eficiente de archivos **PDF y CSV** aplicados a las finanzas de AuraBank.
*   Asegúrate de que la arquitectura propuesta use componentes que se puedan desplegar fácilmente en instancias de **OCI** (como contenedores o servidores de cómputo en la nube).