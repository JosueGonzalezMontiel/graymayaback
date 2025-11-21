"""
Configuración de la aplicación. Carga parámetros desde variables de entorno
usando Pydantic para que sea fácil de tipar y extender. Este archivo se
inspira en el diseño del repositorio original `tep`.
"""

import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

class Settings:
    # Sin valores por defecto sensibles
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    API_KEY: str = os.getenv("API_KEY")
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    


settings = Settings()

# Exportar para compatibilidad con deps.py
API_KEY = settings.API_KEY  # ✅ Ahora deps.py puede importarlo