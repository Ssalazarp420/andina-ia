# 2 - Proceso y extracción de contenido

## Descripción
El procesamiento y extracción de contenido es la fase responsable de transformar los documentos originales —en sus variados formatos— en texto limpio y estructurado, listo para ser convertido en *embeddings* en la siguiente etapa.

Funciona a través de los siguientes pasos estructurados:

---

## 1. Extracción por formato
Cada tipo de archivo exige un enfoque diferente para recuperar la información de manera óptima:
* **PDF:** Extracción de texto directo cuando el PDF es nativo (generado digitalmente). Cuando es un documento escaneado (imagen), es necesario utilizar **OCR** (*Optical Character Recognition*) para convertir la imagen en texto legible.
* **Word:** Extracción del texto corrido, preservando la estructura jerárquica como títulos, subtítulos y párrafos, lo cual ayuda a mantener el sentido al fragmentar el contenido posteriormente.
* **Excel:** Conversión de las tablas en texto estructurado (por ejemplo, línea por línea, repitiendo los encabezados de columna), ya que las planillas tienen una lógica de lectura diferente a la del texto corrido.
* **PowerPoint:** Extracción del texto de cada diapositiva (*slide*), idealmente junto con las notas del orador, las cuales suelen contener contexto adicional de gran importancia.
* **Markdown, CSV, JSON, HTML:** Formatos que ya son estructurados o semiestructurados. Requieren principalmente eliminar marcas técnicas (etiquetas HTML, sintaxis Markdown) manteniendo el contenido legible, o bien convertir la estructura de datos (JSON, CSV) en frases o tablas comprensibles para el modelo.

## 2. Limpieza del texto
Consiste en la eliminación de ruidos que no aportan significado semántico al agente:
* Encabezados y pies de página repetidos.
* Numeración de páginas.
* Caracteres especiales de formato o código oculto.
* Espacios duplicados o saltos de línea huérfanos.
* Fragmentos corrompidos derivados de la extracción (común en PDFs mal formateados).

## 3. Chunking (división en fragmentos)
El texto extraído se divide en partes más pequeñas (*chunks*), ya que los documentos completos suelen ser demasiado grandes para ser procesados eficientemente en la búsqueda y dentro de la ventana de contexto del LLM. Las estrategias más comunes son:
* **Por tamaño fijo:** Fragmentos de longitud determinada (por ejemplo, de 500 a 1000 caracteres), aplicando una pequeña superposición (*overlap*) entre fragmentos contiguos para evitar cortar una idea o frase por la mitad.
* **Por estructura lógica:** División respetando la naturaleza del documento (por sección, por párrafo, por cláusula o por diapositiva), lo que tiende a preservar mejor el sentido completo y la cohesión de la información.

## 4. Atribución de metadatos
Cada fragmento o *chunk* recibe información de contexto que se utilizará posteriormente para el filtrado avanzado y la citación precisa de fuentes:
* **Categoría del documento:** Área de negocio (RH, Financiero, Legal, etc.).
* **Origen:** Nombre del archivo original y ruta/enlace de la fuente.
* **Temporalidad:** Fecha de creación o última actualización del contenido.
* **Gobernanza:** Autor o responsable (*owner*) del documento.
* **Ubicación exacta:** Indicador del punto de origen dentro del archivo (número de página, sección o diapositiva).

---

## Por qué esta etapa es crítica
La calidad de la extracción y del *chunking* es el pilar invisible del proyecto. Cualquier error, omisión o ruido arrastrado en esta fase perjudicará directamente la precisión de la búsqueda vectorial y provocará respuestas incompletas, imprecisas o alucinadas por parte de la IA, sin importar qué tan avanzado sea el modelo de lenguaje utilizado.