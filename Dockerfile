# Usa una imagen oficial de Python
FROM python:3.11-slim

# Instalamos Tesseract y dependencias necesarias
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos todos los archivos de tu proyecto al contenedor
COPY . .

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos el puerto que usará Gunicorn
EXPOSE 8000

# Comando para arrancar la app con Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]