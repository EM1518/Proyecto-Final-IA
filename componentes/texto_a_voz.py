## Elisanna María Martínez Sánchez
## 23-EISN-2-074

"""
Módulo para la conversión de texto a voz.
"""

import os
import tempfile
from gtts import gTTS
from configuracion import DIRECTORIO_AUDIO

class TextoAVoz:
    """
    Clase para manejar la conversión de texto a voz utilizando gTTS.
    """
    def __init__(self, directorio_salida=DIRECTORIO_AUDIO):
        """
        Inicializa el objeto TextoAVoz.
        """
        self.directorio_salida = directorio_salida
        os.makedirs(self.directorio_salida, exist_ok=True)
    
    def texto_a_voz(self, texto, codigo_idioma):
        """
        Convierte texto a voz y guarda el resultado en un archivo.
        """
        if not texto:
            return None
        
        try:
            # Crear un archivo temporal para el audio
            archivo_audio_temp = tempfile.NamedTemporaryFile(
                suffix=".mp3",
                dir=self.directorio_salida,
                delete=False
            )
            
            print(f"Generando audio para: '{texto}' en idioma {codigo_idioma}")
            
            # Convertir texto a voz con gTTS
            tts = gTTS(text=texto, lang=codigo_idioma, slow=False)
            tts.save(archivo_audio_temp.name)
            
            print(f"Archivo guardado en: {archivo_audio_temp.name}")
            
            return archivo_audio_temp.name
        
        except Exception as e:
            print(f"Error en la conversión de texto a voz: {str(e)}")
            return None