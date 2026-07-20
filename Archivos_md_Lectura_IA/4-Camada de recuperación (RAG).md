# 4 - Camada de recuperación (RAG)

## Descripción
La capa de recuperación (Retrieval) es el corazón del sistema RAG (*Retrieval-Augmented Generation*): es el componente encargado de buscar, seleccionar y decidir con precisión qué fragmentos de documentos se le entregarán al modelo de lenguaje (LLM) para que este pueda generar una respuesta informada, verídica y contextualizada.

---

## Fases del proceso de recuperación

1. **Transformación de la pregunta en embedding:** Cuando el colaborador realiza una consulta en lenguaje natural, el sistema toma el texto y lo procesa a través del mismo modelo de *embedding* que se utilizó durante la fase de indexación de los documentos. Esto genera un vector numérico que condensa el significado semántico exacto de la pregunta.

2. **Búsqueda semántica en la base de datos vectorial:** El vector de la consulta se compara en tiempo real con los vectores de todos los fragmentos de documentos almacenados en la base de datos, utilizando una métrica de similitud matemática (como la *similitud de coseno* o la *distancia euclidiana*).  
   La base de datos vectorial devuelve los $N$ fragmentos con mayor proximidad semántica. Esto permite que una pregunta como *¿cuántos días de vacaciones tengo?* localice con éxito un fragmento que detalla la *"política de licencia anual remunerada"*, resolviendo la consulta de forma efectiva aunque no coincidan las palabras clave exactas.

3. **Filtrado por metadados:** Para afinar los resultados, se aplican filtros estructurados utilizando los metadados definidos en la etapa de ingesta. Esto permite restringir la búsqueda únicamente a categorías específicas (por ejemplo, solo documentos de *"RH"* o *"Legal"*) o priorizar exclusivamente los archivos más recientes, descartando de inmediato versiones obsoletas o borradores de políticas previas.

4. **Reclasificación (Reranking):** La búsqueda vectorial inicial es masiva y veloz, por lo que suele configurarse para extraer un número amplio de candidatos (por ejemplo, los 20 fragmentos más cercanos). Posteriormente, estos candidatos pasan por un segundo modelo especializado y mucho más preciso llamado **Reranker**.  
   Este componente reevalúa de manera exhaustiva la relación contextual profunda entre la pregunta y cada fragmento individual, reordenándolos de mayor a menor relevancia real y reteniendo únicamente los más útiles (por ejemplo, el top 3 o 5 final).

5. **Ensamblaje del contexto:** Los fragmentos seleccionados y refinados por el reranker se unifican en un bloque de texto estructurado. A cada fragmento se le adjuntan sus metadados de origen (nombre del documento, sección, fecha de actualización). Este bloque consolidado constituye el **contexto enriquecido** que se inyectará directamente dentro del *prompt* que se enviará al LLM para la generación final de la respuesta.

---

## Por qué importa la reclasificación (Reranking)
La búsqueda vectorial pura es excelente para buscar a gran velocidad entre millones de registros, pero puede traer resultados ligeramente desviados del objetivo debido a que mide la similitud general del espacio semántico. 

El **Reranker** actúa como un filtro de precisión quirúrgica: analiza la sintaxis y la relación detallada entre la pregunta y el fragmento. Implementar esta arquitectura híbrida ofrece el equilibrio perfecto para un entorno corporativo: **velocidad extrema** (gracias a la búsqueda vectorial amplia) combinada con una **máxima fidelidad y calidad** (gracias a la reclasificación sobre el conjunto reducido de candidatos).