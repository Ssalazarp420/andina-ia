# 8 - Registrar ejecución del proyecto

## Descripción
El registro de ejecución documenta detalladamente la operación del agente tanto en entornos de prueba como en producción. Su propósito central es habilitar la auditoría, la depuración y la mejora continua del sistema. 

*Nota indispensable de entrega:* Es mandatorio ejecutar esta fase en la nube (OCI u otra plataforma seleccionada) y adjuntar al reporte evidencias o registros multimedia (fotografías, capturas de pantalla o videos) que constaten dicha ejecución exitosa en el entorno productivo.

---

## Modelos de registro según el entorno

### 1. Ejecución local
Cuando el agente corre de forma aislada en la máquina del desarrollador o en un servidor interno sin orquestación de nube, la arquitectura de registro es directa:
* **Logs (Registros de eventos):** Se escriben en archivos de texto locales (comúnmente en formato `.jsonl` o JSON Lines). Capturan de manera secuencial: la pregunta del colaborador, el contexto exacto recuperado, la respuesta generada por el LLM, la marca de tiempo (*timestamp*) y los milisegundos de latencia.
* **Gestión de versiones:** Uso estricto de Git para el control del código fuente, complementado opcionalmente con herramientas como **DVC** (*Data Version Control*) para rastrear el historial de versiones de los documentos indexados y los archivos de *embeddings*.
* **Monitoreo:** Paneles visuales mínimos (como una pestaña interna de Streamlit o Dash) que leen y grafican los datos directamente de los archivos de log locales, sin requerir infraestructura adicional.
* **Balance:** Ofrece bajo costo y control total de datos (ideal para Prototipos y POCs), pero carece de escalabilidad automática y alta disponibilidad.

### 2. Ejecución en la nube (Requisito Obligatorio)
Cuando el agente se despliega de manera formal en una nube gestionada como OCI, el registro se transforma en una solución empresarial centralizada y robusta:
* **Logs Centralizados:** Redirección automática de la salida estándar hacia servicios nativos de observabilidad (como *OCI Logging*, CloudWatch o Google Cloud Logging). Permite indexación avanzada, retención de historial configurable por políticas de cumplimiento y alertas automáticas ante fallas críticas.
* **Trazabilidad de Experimentos:** Almacenamiento sistemático de las versiones exactas de los modelos de lenguaje utilizados, la plantilla del *prompt* maestro, el estado del índice vectorial y los hiperparámetros de temperatura/tokens aplicados en cada inferencia.
* **Paneles de Observabilidad:** Cuadros de mando integrados para supervisar métricas clave en tiempo real: latencia de la base de datos vectorial, tasas de error HTTP (5xx/4xx), costo financiero acumulado por petición y consumo de tokens de entrada/salida.
* **Balance:** Aporta escalabilidad elástica, respaldos (*backups*) automatizados e integración con flujos corporativos de CI/CD, con la contraparte de un costo recurrentes y una configuración de red y gobernanza de datos más rigurosa.

---

## Por qué importa esta etapa
El objetivo final de esta fase no es solo acumular datos, sino garantizar la **trazabilidad de extremo a extremo** (saber con certeza quién preguntó qué, qué fragmento exacto de qué documento se inyectó como contexto, y qué respuesta textual emitió el modelo). Contar con este nivel de auditoría blinda legalmente a la organización y provee los datos empíricos necesarios para optimizar la inteligencia del agente a lo largo del tiempo.