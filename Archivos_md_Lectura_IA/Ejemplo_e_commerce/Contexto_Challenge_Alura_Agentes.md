# Especificación de Proyecto: AuraBank Copilot (Challenge Alura Agentes)

Este documento centraliza el contexto de negocio, los requerimientos técnicos y la arquitectura documental del proyecto **AuraBank Copilot**. Actúa como la directriz principal en NotebookLM para guiar el desarrollo de un agente de Inteligencia Artificial corporativo enfocado al 100% en el sector Fintech y Banca Digital.

---

## 1. Identidad del Proyecto y de la Empresa
*   **Nombre del Proyecto:** AuraBank Copilot
*   **Empresa Ficticia:** AuraBank (Plataforma nativa de banca digital, billeteras electrónicas y servicios financieros integrados).
*   **Misión del Agente:** Actuar como un copiloto conversacional centralizado, seguro y siempre disponible para resolver de manera inmediata cualquier duda de los colaboradores de AuraBank sobre normativas financieras, flujos operativos, límites de cuentas y tarifas transaccionales.

---

## 2. Origen del Contexto y Adaptación Financiera
El marco base del desafío está inspirado formalmente en la estructura transaccional de los ejemplos del challenge de Alura (como los flujos de cobros y reembolsos). No obstante, para elevar la complejidad técnica hacia el ecosistema **Fintech**, toda la documentación e información se ha migrado e independizado bajo la marca corporativa de **AuraBank**, asegurando un enfoque riguroso en finanzas digitales y seguridad de la información.

---

## 3. Requisitos Mandatorios de Alura
Para garantizar la validez del proyecto dentro del desafío, el entregable debe cumplir estrictamente tres condiciones:
1.  **Repositorio Público en GitHub:** Código fuente documentado, prompts, e ingestion pipelines limpios.
2.  **Despliegue en la Nube de Oracle (OCI):** Hospedaje y ejecución del agente consumiendo activamente al menos un servicio oficial de Oracle Cloud Infrastructure (OCI).
3.  **Evidencia en README:** Imagen o video demostrativo del agente operando en producción dentro de OCI.

---

## 4. Estrategia Multiformato de la Base de Conocimiento (Los 8 Formatos)
El agente de IA corporativo debe procesar de forma nativa e híbrida la documentación interna del banco, la cual está fragmentada intencionalmente en los 8 formatos requeridos por el challenge para demostrar la robustez del sistema:

| # | Documento Corporativo de AuraBank | Formato | Rol Estratégico en el Agente |
|---|-----------------------------------|---------|-------------------------------------------------------------------|
| 1 | **Preguntas Frecuentes sobre Métodos de Pago y Pasarelas** | `.pdf` | Reglas de dispersión de fondos, contracargos y fraudes con tarjetas. |
| 2 | **Política General de Reembolsos y Ajustes de Cuenta** | `.docx` | Manual de operaciones legales y regulatorias para la devolución de capital. |
| 3 | **Matriz de Tarifas, Comisiones Bancarias y Tasas** | `.xlsx` | Datos numéricos tabulares de alta precisión (tasas de interés, cobros interbancarios). |
| 4 | **Límites Globales de Transacciones Diarias** | `.csv` | Datos planos indexados con montos máximos permitidos por tipo de wallet o cuenta. |
| 5 | **Programa de Fidelidad "AuraPoints" y Beneficios** | `.pptx` | Presentación institucional de beneficios cruzados para usuarios activos. |
| 6 | **Manual Operativo de Garantías y Contratos de Depósito** | `.md` | Guías rápidas y documentación de ingeniería para soporte técnico del core bancario. |
| 7 | **Estructura de Errores Comunes de la API Financiera** | `.json` | Estructuras de llave-valor para consultas rápidas sobre fallos en integraciones web. |
| 8 | **Portal Interno de Autogestión para el Colaborador** | `.html` | Réplica del sitio web de soporte interno con normativas de ciberseguridad. |

---

## 5. Directiva de Comportamiento para NotebookLM
Al interactuar con esta base de conocimiento, la IA debe comprender que:
*   Cualquier código, prompt o contenido documental que se genere de aquí en adelante debe pertenecer orgánicamente a **AuraBank** y alinearse a un lenguaje corporativo, seguro, financiero y tecnológico.
*   El agente operará combinando recuperación semántica estándar para textos densos (`.pdf`, `.docx`, `.md`) con consultas ultra-precisas para archivos de datos tabulares (`.xlsx`, `.csv`, `.json`).