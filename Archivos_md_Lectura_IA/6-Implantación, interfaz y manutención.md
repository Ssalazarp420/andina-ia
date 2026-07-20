# 6 - Implantación, interfaz y manutención

## Descripción
Esta fase final abarca el despliegue del agente a través de un canal accesible para los colaboradores y el establecimiento de los procesos de mantenimiento continuo. La interfaz no requiere de un diseño sofisticado o un desarrollo de *front-end* profesional; el objetivo central del proyecto es la funcionalidad, simplicidad y eficiencia de la herramienta.

---

## Construcción de la interfaz
La elección del canal debe alinearse con el entorno digital donde los colaboradores ya realizan sus actividades diarias. Las opciones más recomendadas son:
* **Chat web dedicado:** Una página interna simple (por ejemplo, desarrollada con **Streamlit**). Es la opción más rápida de implementar y contiene un campo para escribir preguntas, historial de chat y visualización clara de las fuentes citadas.
* **Integración con herramientas de comunicación:** Un bot integrado directamente dentro de **Microsoft Teams** o **Slack**. Esta alternativa resulta muy natural para el usuario, ya que evita tener que abrir un sistema adicional.
* **Plugin en portales existentes:** Incorporar al agente como un *widget* interactivo dentro de la intranet corporativa o el portal de Recursos Humanos ya existente.

### Elementos esenciales de la interfaz
Independientemente del canal seleccionado, la interfaz debe contar con:
1. **Transparencia:** Una indicación explícita de que el usuario está interactuando con un agente de Inteligencia Artificial y no con un humano.
2. **Evidencia y Trazabilidad:** Bloques de texto o enlaces interactivos que muestren las fuentes y documentos específicos utilizados para construir la respuesta.
3. **Módulo de Feedback:** Botones de retroalimentación simple (pulgar arriba / pulgar abajo) integrados en cada respuesta para recolectar la percepción del usuario.
4. **Persistencia del Contexto:** Un historial de conversación que permita mantener el hilo y el contexto dentro de la misma sesión de chat.

---

## Mantenimiento continuo
El mantenimiento es el proceso que garantiza que el agente siga siendo relevante, preciso y confiable a lo largo del tiempo, evitando que la base de conocimientos quede obsoleta.

* **Pipeline de actualización automática:** Siempre que un documento sea creado, modificado o eliminado en las fuentes originales (Google Drive, SharePoint, etc.), un proceso automatizado debe detectar el cambio, reprocesar el archivo y actualizar el índice vectorial de forma periódica (diaria o semanal).
* **Gobernanza y curaduría de contenido:** Los responsables asignados a cada categoría (*owners* de RH, Financiero, Legal) deben revisar periódicamente que los documentos indexados correspondan a la versión oficial vigente, eliminando archivos obsoletos.
* **Monitoreo de calidad y analítica:** Seguimiento constante a métricas críticas de rendimiento técnico y de negocio:
  * Tasa de preguntas sin respuesta (*Fallbacks*).
  * Volumen y motivos de retroalimentación negativa.
  * Tiempos de respuesta (latencia del LLM y de la base de datos).
* **Ciclo de mejora incremental:** Las preguntas recurrentes que el agente no logre responder con éxito sirven como indicadores directos de vacíos de información, lo que señala la necesidad de redactar e indexar nuevos documentos normativos. Las respuestas con bajas calificaciones ayudan a ajustar el *prompting* o la lógica de la capa de recuperación.
* **Actualización y evaluación de modelos:** Monitorear el mercado para identificar si nuevas versiones de LLMs o modelos de *embedding* ofrecen un desempeño superior en costo o precisión, realizando pruebas (*A/B testing*) antes de cualquier migración en producción.

---

## Herramientas recomendadas
Si optas por un chat web dedicado, **Streamlit** es una excelente alternativa para construir interfaces de datos rápidamente en Python sin dolores de cabeza. Permite desplegar un prototipo completamente funcional, interactivo y conectado a tu pipeline de RAG en cuestión de horas.