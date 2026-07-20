# 3 - Indexación

## Descripción
La indexación vectorial es el proceso de transformar el texto extraído de los documentos en representaciones numéricas que capturan su significado semántico, organizándolas de forma que puedan ser buscadas rápidamente por similitud. Es lo que hace posible, en la etapa 4, encontrar fragmentos relevantes incluso cuando la pregunta del colaborador no utiliza exactamente las mismas palabras que contiene el documento.

---

## ¿Qué es un embedding?
Un *embedding* es un vector de números (generalmente de cientos o miles de dimensiones) generado por un modelo de lenguaje entrenado específicamente para este propósito.

Los textos con significados parecidos generan vectores numéricamente próximos en el espacio multidimensional, incluso si utilizan palabras completamente diferentes. Por ejemplo, *"política de reembolso de gastos"* y *"cómo solicitar el resarcimiento de costos"* tienden a generar vectores cercanos porque el modelo comprende que tratan sobre el mismo tema subyacente.

---

## Cómo funciona en este proyecto (Paso a paso)

1. **Entrada:** Cada fragmento (*chunk*) de texto generado en la etapa 2 (ya limpio y con sus metadados asociados) se envía a un modelo de embedding especializado.
2. **Generación del vector:** El modelo procesa el fragmento y devuelve un vector numérico que lo representa. Es fundamental utilizar este mismo modelo de forma consistente tanto para la indexación de los documentos como para las preguntas de los colaboradores; los vectores generados por modelos diferentes no son compatibles ni comparables entre sí.
3. **Almacenamiento:** El vector se almacena en una **base de datos vectorial** junto con una referencia al texto original y todos sus metadados (categoría, nombre del archivo, fecha, autor). Dependiendo de la infraestructura de la empresa, las opciones más comunes incluyen:
   * Pinecone
   * Weaviate
   * Qdrant
   * Chroma
   * pgvector (extensión de PostgreSQL)
4. **Indexación para búsqueda eficiente:** La base de datos vectorial organiza estos vectores en una estructura de índice optimizada (como **HNSW** — *Hierarchical Navigable Small World*). Esto permite encontrar los vectores más cercanos a una consulta en milisegundos, sin necesidad de compararlos uno por uno con todos los millones de vectores almacenados, lo cual sería inviable a escala.
5. **Indexación paralela de metadados:** Además de la búsqueda vectorial, los metadados se indexan de forma tradicional (relacional o documental). Esto permite aplicar **filtros híbridos** —por ejemplo, restringir la búsqueda únicamente a documentos de la categoría *"Financiero"* creados en los últimos 12 meses— agilizando el proceso y aumentando la precisión antes o durante el cálculo de la similitud semántica.

---

## Por qué importa esta etapa
La indexación vectorial unifica documentos de diferentes formatos y categorías en un único espacio de búsqueda común. Permite que una sola consulta realice una búsqueda semántica profunda en toda la base de conocimiento de la empresa, mientras que los metadados garantizan el control, la gobernanza y la capacidad de restringir dicha búsqueda a un contexto específico cuando sea necesario.