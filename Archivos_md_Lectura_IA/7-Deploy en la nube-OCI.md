# 7 - Deploy en la nube - OCI

## Descripción
Con el agente validado localmente en los pasos anteriores, esta etapa cubre la publicación y puesta en marcha del sistema dentro de **Oracle Cloud Infrastructure (OCI)**, haciéndolo accesible para todos los colaboradores de forma estable, segura y escalable. 

---

## ¿Qué es el Deploy (Despliegue)?
En el contexto del desarrollo de software e IA, el *deploy* o despliegue es el proceso de trasladar el agente desde la máquina local del desarrollador hacia un entorno de producción en la nube. Esto permite que el sistema opere de forma continua, asíncrona y accesible para múltiples usuarios de manera simultánea a través de internet o de la red corporativa.

---

## Arquitectura y servicios sugeridos en OCI
Para garantizar una infraestructura robusta, se presentan las siguientes recomendaciones de servicios dentro del ecosistema de OCI (recordando que, de acuerdo con los requerimientos del proyecto, **es obligatorio implementar al menos un servicio de OCI**):

* **Contenerización (OCI Container Registry - OCIR):** Empaquetar la aplicación completa (API del agente, lógica de RAG y todas sus dependencias de librerías) en una imagen de Docker. Esta imagen se almacena de forma privada y segura en el registro de contenedores administrado de Oracle.
* **Capa de Cómputo (Compute / Container Instances / OKE):** Dependiendo de la complejidad y el presupuesto, se puede optar por:
  * *OCI Compute:* Instancias de máquinas virtuales (VM) tradicionales y sencillas.
  * *OCI Container Instances:* Ejecución directa de contenedores sin la necesidad de gestionar o parchar el sistema operativo de una VM subyence.
  * *OKE (Oracle Kubernetes Engine):* Orquestación avanzada basada en Kubernetes, ideal para escalamiento automático elástico basado en el volumen de peticiones o preguntas concurrentes de los colaboradores.
* **Almacenamiento de documentos (OCI Object Storage):** Los archivos originales provistos por las áreas de negocio (PDF, Word, Excel, etc.) se almacenan en *buckets* de Object Storage. El acceso a estos datos queda estrictamente restringido mediante políticas de **IAM (Identity and Access Management)** de OCI.
* **Base de datos vectorial (Oracle Autonomous Database):** Hospedar los vectores utilizando las capacidades de búsqueda vectorial nativa (*AI Vector Search*) de Oracle Autonomous Database, o bien desplegar una solución vectorial dedicada (como Qdrant o Weaviate) sobre Compute/OKE, asegurando la sincronización entre los *embeddings* y los archivos en Object Storage.
* **Gestión de Secretos (OCI Vault):** Las llaves de API externas (como los tokens del proveedor de LLM) y las cadenas de conexión a las bases de datos se guardan de forma cifrada en OCI Vault, evitando que queden expuestas en texto plano dentro del código o en variables de entorno abiertas.
* **Red y Seguridad (VCN & Load Balancer):** Configuración de una red virtual en la nube (**Virtual Cloud Network - VCN**) segmentada con subredes públicas y privadas. Se integra un *Load Balancer* (Balanceador de carga) para distribuir el tráfico de peticiones y *Network Security Groups* (NSGs) para blindar los puertos abiertos.
* **Automatización (CI/CD):** Creación de un pipeline de despliegue continuo (utilizando OCI DevOps o herramientas externas como GitHub Actions) que automatice la compilación de la imagen de Docker, ejecute pruebas unitarias y realice el despliegue automático ante cualquier actualización en el código base.

---

## Por qué importa esta etapa
El despliegue en la nube transforma un prototipo de laboratorio en un producto empresarial real. Al delegar la infraestructura a una nube como OCI, se garantiza que el agente de IA cuente con alta disponibilidad, redundancia ante fallas y la capacidad de escalar sus recursos computacionales a medida que la organización cargue más documentos o incremente su base de usuarios activos.