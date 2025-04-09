## Elisanna María Martínez Sánchez
## 23-EISN-2-074

"""
Configuraciones globales para la aplicación 
"""

import os
from dotenv import load_dotenv
import pathlib

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Directorio raíz del proyecto
DIRECTORIO_RAIZ = pathlib.Path(__file__).parent.absolute()

# Directorios de recursos
DIRECTORIO_ACTIVOS = os.path.join(DIRECTORIO_RAIZ, "activos")
DIRECTORIO_AUDIO = os.path.join(DIRECTORIO_ACTIVOS, "audio")
DIRECTORIO_IMAGENES = os.path.join(DIRECTORIO_ACTIVOS, "imagenes")

# Crear directorios si no existen
os.makedirs(DIRECTORIO_AUDIO, exist_ok=True)
os.makedirs(DIRECTORIO_IMAGENES, exist_ok=True)

# Clave API de OpenAI
CLAVE_API_OPENAI = os.getenv("OPENAI_API_KEY")

# Configuración básica
TASA_MUESTREO = 16000  # Frecuencia de muestreo en Hz

# Idiomas soportados 
IDIOMAS_SOPORTADOS = {
    "español": "es",
    "inglés": "en"
}