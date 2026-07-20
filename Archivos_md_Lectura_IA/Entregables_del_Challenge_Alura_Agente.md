# Entregables del Challenge Alura Agente

## Descripción
Este documento detalla los requisitos técnicos obligatorios y los entregables oficiales que componen la entrega final del desafío **Alura Agentes**. El cumplimiento estricto de cada uno de estos elementos es indispensable para validar el éxito de la solución implementada.

---

## 📋 Lista de Componentes Obligatorios

### 1. Repositorio en GitHub
El código fuente completo de la solución debe estar centralizado bajo las siguientes pautas:
* **Acceso:** El repositorio debe estar configurado como **público** para permitir su evaluación.
* **Trazabilidad:** Un historial de *commits* limpio y descriptivo que refleje fielmente el progreso y la evolución del desarrollo del proyecto.
* **Buenas Prácticas:** Una estructura de directorios organizada, estandarizada y fácil de comprender por otros desarrolladores (ej. separar la lógica de la API, la interfaz y los scripts de ingestión).

### 2. Documentación Técnica (README.md)
La raíz del repositorio debe contar con un archivo `README.md` exhaustivo y profesional que actúe como la carta de presentación técnica del sistema. Debe incluir obligatoriamente:
* **Descripción General:** Resumen ejecutivo del problema de negocio que resuelve el agente.
* **Arquitectura de la Solución:** Diagrama o explicación detallada del flujo del pipeline (Ingesta $\rightarrow$ Chunking $\rightarrow$ Embedding $\rightarrow$ Recuperación $\rightarrow$ Generación LLM).
* **Stack Tecnológico:** Listado de todas las tecnologías, librerías, modelos de lenguaje y bases de datos vectoriales utilizadas.
* **Guía de Despliegue Local:** Instrucciones paso a paso para clonar, configurar variables de entorno y ejecutar el proyecto de manera local.
* **Casos de Prueba (QA):** Ejemplos reales de preguntas complejas que el agente es capaz de resolver junto con las respuestas estructuradas que el sistema generó, incluyendo la citación de sus fuentes.

### 3. Agente Inteligente Funcional
El núcleo de software del proyecto debe demostrar capacidades cognitivas reales aplicadas a la empresa:
* **Procesamiento de Documentos:** Inclusión del código fuente específico encargado de la lectura, limpieza y extracción semántica de archivos en formatos como `PDF` o `CSV`.
* **Resolución Semántica:** Capacidad del agente para interpretar consultas en lenguaje natural y responder de manera precisa basándose únicamente en el contenido de los documentos provistos como fuente oficial.

### 4. ☁️ Evidencia del Deploy en OCI (Oracle Cloud Infrastructure)
Es mandatorio demostrar de forma empírica que el sistema ha salido del entorno de desarrollo local y se encuentra operativo en una infraestructura de nube real. Se debe proveer al menos uno de los siguientes respaldos:
* **Acceso en Vivo:** El enlace o URL pública de la aplicación desplegada y lista para ser probada.
* **Evidencia Multimedia:** Capturas de pantalla claras o grabaciones de video insertadas directamente en el `README.md` que muestren la interfaz del agente respondiendo preguntas de forma exitosa desde el servidor en la nube de OCI.

---

## 🎯 Criterio de Éxito
Un proyecto se considera aprobado cuando un tercero puede clonar el repositorio de GitHub, entender la arquitectura gracias al README, revisar el código del pipeline de datos y validar la ejecución final a través de las evidencias del despliegue en OCI.