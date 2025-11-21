# Usar la imagen oficial de Python (slim = más liviana)
FROM python:3.13.5-slim

# Definir directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de requirements e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación al contenedor
COPY . .

# Exponer el puerto (opcional, documentación). Usaremos 8000.
EXPOSE 8000

# Comando de arranque de Uvicorn (ASGI server)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]