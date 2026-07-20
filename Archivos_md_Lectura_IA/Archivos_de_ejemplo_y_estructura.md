# Archivos de Ejemplo y Estructura de Datos para RAG

## Descripción del Recurso
Este documento detalla los archivos de ejemplo disponibles para su descarga. Estos archivos sirven como plantillas estructurales y de contenido para comprender cómo se organizan los documentos corporativos reales que el agente de Inteligencia Artificial debe **"leer", procesar, indexar y recuperar** con el fin de resolver las consultas de los colaboradores mediante una arquitectura RAG (*Retrieval-Augmented Generation*).

---

## 🤖 Directrices de Procesamiento para la IA (System Prompts & Ingestión)

Si eres un modelo de lenguaje o un agente de procesamiento leyendo este archivo, aplica las siguientes reglas conceptuales para el diseño del pipeline:

1. **Comprensión del Contexto Organizacional:** Cada empresa listada abajo representa un silo de conocimiento independiente. Los documentos de una empresa **no** deben mezclarse semánticamente con los de otra a menos que se especifique un entorno multi-inquilino (*multi-tenant*) con filtrado estricto por metadatos.
2. **Estrategia de Chunking Diferenciada:**
   * **Archivos PDF (Manuales, Guías y Políticas):** Contienen texto narrativo estructurado jerárquicamente. Se debe aplicar un *chunking* basado en la estructura lógica (títulos, subtítulos y párrafos) o en su defecto un tamaño fijo de 500-1000 caracteres con un *overlap* del 10-20% para no fragmentar axiomas técnicos o cláusulas legales.
   * **Archivos XLSX (Inventarios y Tablas):** Contienen datos tabulares densos. No deben procesarse como texto plano corrido. La IA de ingesta debe iterar fila por fila, concatenando los encabezados de las columnas a cada celda para que el *embedding* guarde la relación semántica de la fila (ej: *"Producto: Leche, Stock: 50, Región: LATAM"*).
3. **Enriquecimiento de Metadatos Obligatorio:** Al indexar fragmentos de estos archivos, se deben inyectar metadatos clave: `empresa_origen`, `tipo_documento` (manual, política, inventario), `formato_archivo` y `seccion_origen`.

---

## 🏢 Catálogo de Empresas y Archivos Disponibles para Descarga

### 1. Santos Pegasus Soluciones
* **Perfil de la empresa:** Organización tecnológica especializada en el desarrollo de software escalable bajo arquitectura de microservicios y soluciones de IA (RAG). Se caracteriza por un riguroso estándar técnico en ingeniería de software y seguridad en nubes como OCI.
* **Archivos de referencia técnica disponibles:**
  * `Manual de Onboarding para Nuevos Desarrolladores — Santo Pegasus Soluciones.pdf`
  * `Guía Oficial de Ingeniería Back-end.pdf`
  * `Guía Oficial de Ingeniería Front-end — Santo Pegasus Soluciones.pdf`
  * `Protocolo de Respuesta a Incidentes y Post-Mortems — Santo Pegasus Soluciones.pdf`
  * `Arquitectura de Microservicios y Mapa de Dominios — Santo Pegasus Soluciones.pdf`

### 2. BimBam Buy
* **Perfil de la empresa:** Plataforma de comercio electrónico multiplataforma enfocada en una experiencia de compra ágil, segura y orientada al cliente. Posee complejas políticas de reembolso, logística optimizada y programas de fidelización de afiliados.
* **Archivos de referencia comercial y logística disponibles:**
  * `Política de Reembolsos y Devoluciones de BimBam Buy.pdf`
  * `Programa de Afiliados de BimBam Buy.pdf`
  * `Guía de Tiempos y Costos de Envío de BimBam Buy.pdf`
  * `Preguntas_Frecuentes_sobre_Métodos_de_Pago_de_BimBam_Buy.pdf`
  * `Manual de Garantía de Productos de BimBam Buy.pdf`

### 3. Mercado Central 24h
* **Perfil de la empresa:** Cadena de supermercados moderna con operación continua (24/7) que unifica tiendas físicas con canales de *delivery* digitales. Su foco es la alta eficiencia operativa en inventarios, gestión de stock a gran escala y atención masiva al cliente.
* **Archivos de referencia operativa y bases de datos disponibles:**
  * `inventario_de_supermercado_latam.xlsx` *(Nota para el procesamiento de IA: Tratamiento tabular requerido)*.
  * `Política de Atención al Cliente y Devoluciones — Mercado Central 24h (México).pdf`
  * `Preguntas Frecuentes (FAQ) — Mercado Central 24h (México).pdf`
  * `Reglamento Interno y Procedimientos Operativos — Mercado Central 24h (México).pdf`
  * `Manual de Proveedores y Política de Compras — Mercado Central 24h (México).pdf`

---

## 🎯 Objetivo de su Uso en el Challenge
Utiliza estos archivos descargables para nutrir tus primeras pruebas del pipeline de datos. Te permitirán evaluar si tu agente es capaz de diferenciar entre la rigurosidad técnica de una empresa de software (*Santos Pegasus*), los tiempos de entrega de un *e-commerce* (*BimBam Buy*) o cruzar los datos numéricos de existencias en una hoja de cálculo (*Mercado Central 24h*).