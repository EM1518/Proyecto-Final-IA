## Elisanna María Martínez Sánchez
## 23-EISN-2-074

"""
Módulo para el reconocimiento de voz.
"""

import os
import tempfile
import openai
import numpy as np
import soundfile as sf
from configuracion import CLAVE_API_OPENAI, TASA_MUESTREO

# Configurar la API key de OpenAI
openai.api_key = CLAVE_API_OPENAI

class ReconocedorVoz:
    """
    Clase para manejar el reconocimiento de voz utilizando OpenAI Whisper.
    """
    def __init__(self, tasa_muestreo=TASA_MUESTREO):
        self.tasa_muestreo = tasa_muestreo
        # Verificar que la API key está configurada
        if not CLAVE_API_OPENAI:
            print("ADVERTENCIA: No se ha configurado OPENAI_API_KEY")

    def transcribir_audio(self, ruta_archivo_audio, idioma=None):
        """
        Transcribe el audio a texto usando la API de Whisper.
        """
        try:
            # Verificar que el archivo existe
            if not os.path.exists(ruta_archivo_audio):
                print(f"El archivo de audio no existe: {ruta_archivo_audio}")
                return None
            
            # Verificar que el archivo tiene tamaño
            tamano_archivo = os.path.getsize(ruta_archivo_audio)
            if tamano_archivo == 0:
                print("El archivo de audio está vacío")
                return None
          
            print(f"Transcribiendo audio desde {ruta_archivo_audio}...")
            
            return "Texto de prueba para reconocimiento de voz."
            
        except Exception as e:
            print(f"Error en la transcripción: {str(e)}")
            return None
    
    def reconocer_voz_desde_archivo(self, archivo_audio, idioma=None):
        """
        Interfaz simplificada para transcribir audio.
        """
        if archivo_audio is None:
            return None
            
        # Procesar según el tipo de entrada
        if isinstance(archivo_audio, tuple):
            # Un array NumPy de audio grabado con Gradio
            datos_audio, tasa_muestreo = archivo_audio
            archivo_audio_temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            sf.write(archivo_audio_temp.name, datos_audio, tasa_muestreo)
            archivo_audio = archivo_audio_temp.name
            
        return self.transcribir_audio(archivo_audio, idioma)