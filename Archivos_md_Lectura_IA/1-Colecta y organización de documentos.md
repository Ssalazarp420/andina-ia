# 1 - Colecta y organización de documentos

## Descripción
La recolección y organización de los documentos es el punto de partida de todo el proyecto: antes de procesar, indexar o buscar cualquier cosa, es necesario saber exactamente qué documentos existen, dónde están y quién es responsable de ellos.

Es una etapa más organizacional que técnica, pero que determina la calidad de todo lo que viene después.

---

## 1. Mapeo de las fuentes
El primer paso es descubrir dónde están hoy los documentos relevantes, ya que en una empresa suelen estar dispersos en:
* **Carpetas compartidas:** Google Drive, SharePoint, OneDrive.
* **Sistemas internos:** Sistema de Recursos Humanos.
* **Repositorios de código:** Para documentación técnica.
* **Correos electrónicos:** Archivados.
* **Almacenamiento local:** Carpetas locales en computadoras de personas clave.

Este mapeo generalmente requiere hablar con cada área (RH, Financiero, Jurídico, etc.) para entender dónde guardan sus documentos oficiales.

## 2. Definición de categorías
Los documentos se organizan en las categorías de negocio que tengan sentido para la empresa —como las sugeridas al inicio del proyecto (RH, Financiero, Operacional, Legal, etc.).

Esta categorización no es solo cosmética: se convierte en un **metadato** que se utilizará después para filtrar búsquedas y para definir a los responsables de mantener actualizado ese conjunto de documentos.

## 3. Curaduría de calidad
No todo documento encontrado debe ingresar a la base. En esta fase es importante filtrar:
* **Versiones desactualizadas o borradores:** Manteniendo solo la versión oficial vigente de una política, por ejemplo.
* **Documentos duplicados o redundantes:** Eliminación de copias innecesarias.
* **Contenido irrelevante:** Notas personales o archivos de prueba que no aporten valor a las preguntas de los colaboradores.

## 4. Definición de responsables (*ownership*)
Cada categoría de documentos debe tener un responsable dentro de la empresa —generalmente alguien de la propia área (RH se encarga de los documentos de RH, el área Jurídica se encarga de contratos y compliance).

Esta persona es quien aprueba lo que entra a la base y a quien se le debe avisar cuando el contenido necesite una actualización.

## 5. Acceso y permisos
Como se definió en el proyecto, el agente está abierto a todos los colaboradores, por lo que aquí el enfoque no es restringir quién puede preguntar, sino garantizar que el agente tenga **acceso de lectura** a los lugares correctos (carpetas, sistemas) para buscar y actualizar los documentos automáticamente, sin depender del envío manual de archivos.

## 6. Proceso de ingesta inicial
Por último, se define cómo llegarán esos documentos al pipeline de procesamiento (etapa 2):
* **Vía conexión directa con la fuente:** Por ejemplo, la API de Google Drive o SharePoint.
* **Carga (*upload*) manual inicial:** Para comenzar el proyecto de forma inmediata.
* **Enfoque híbrido:** Una combinación de ambas opciones mientras se construye la integración automática.

---

## Por qué esta etapa importa tanto
Si esta base se estructura de forma deficiente —con documentos desactualizados, mal categorizados o sin un responsable definido— todo el resto del pipeline (procesamiento, indexación, búsqueda, generación de respuesta) heredará ese problema.

Es el principio de **"garbage in, garbage out"** (si entra basura, sale basura): la IA solo puede ser tan confiable como los documentos de los que se alimenta.