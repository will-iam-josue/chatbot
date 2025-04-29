# Usa una imagen oficial de Python
FROM python:3.11-slim

# Instalamos Tesseract y dependencias necesarias
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Directorio de trabajo dentro del contenedor
WORKDIR /chatbot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copiamos todos los archivos de tu proyecto al contenedor
COPY ./__pycache__/ /chatbot/__pycache__/
COPY ./docs/ /chatbot/docs/
COPY ./instance/ /chatbot/instance/
COPY ./templates/ /chatbot/templates
COPY api.py /chatbot/
COPY app.py /chatbot/
COPY Dockerfile /chatbot/
COPY README.md /chatbot/
COPY render.yaml /chatbot/
COPY requirements.txt /chatbot/

# Actualizamos pip
RUN pip install --upgrade pip

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos el puerto que usará Gunicorn
EXPOSE 8000

# Comando para arrancar la app con Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]