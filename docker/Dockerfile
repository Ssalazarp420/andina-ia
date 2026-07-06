# Imagen para Andina IA — pensada para OCI Container Registry (OCIR)
# y ejecución en OCI Container Instances / OKE.

FROM python:3.11-slim

WORKDIR /app

# Dependencias del sistema necesarias para pdfplumber / OCR (si se agrega luego)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

# Variables de entorno reales se inyectan en runtime vía OCI Vault / env vars del contenedor,
# nunca se hardcodean ni se copian en la imagen.

CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
