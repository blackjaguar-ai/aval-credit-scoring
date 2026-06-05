# ──────────────────────────────────────────────────────────────
# AVAL — Dockerfile
# Imagen liviana. XGBoost no necesita las dependencias de deep learning.
# Build: docker build -t aval-credit-scoring:latest .
# ──────────────────────────────────────────────────────────────

FROM python:3.11-slim

# Metadatos
LABEL maintainer="Cristian"
LABEL project="aval-credit-scoring"
LABEL description="API de scoring crediticio alternativo para thin-file"

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Instalar dependencias del sistema (mínimas para compilar algunas librerías)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar y instalar dependencias primero (cache layer de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY src/ ./src/
COPY api/ ./api/
COPY configs/ ./configs/
COPY models/ ./models/

# Puerto que expone la API
EXPOSE 8000

# Health check: el contenedor reporta su propio estado
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health').raise_for_status()"

# Arranque: modelo cargado al inicio, no por request
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]