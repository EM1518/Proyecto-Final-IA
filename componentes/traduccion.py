## Elisanna María Martínez Sánchez
## 23-EISN-2-074

"""
Módulo para la traducción de texto.
"""

import openai
from configuracion import CLAVE_API_OPENAI, MODELO_GPT

# Configurar la API key de OpenAI
openai.api_key = CLAVE_API_OPENAI

class Traductor:
    """
    Clase para manejar la traducción de texto utilizando la API de OpenAI.
    """
    def __init__(self, modelo=MODELO_GPT):
        self.modelo = modelo
        # Verificar que la API key está configurada
        if not CLAVE_API_OPENAI:
            print("ADVERTENCIA: No se ha configurado OPENAI_API_KEY")

    def traducir(self, texto, idioma_origen, idioma_destino):
        """
        Traduce el texto del idioma de origen al idioma de destino
        """
        if not texto:
            return ""
        
        try:
            
            print(f"Traduciendo de {idioma_origen} a {idioma_destino}: {texto}")
            
            # Simulación de traducción para pruebas 
            if idioma_origen.lower() == "español" and idioma_destino.lower() == "inglés":
                return "This is a test translation from Spanish to English."
            elif idioma_origen.lower() == "inglés" and idioma_destino.lower() == "español":
                return "Esta es una traducción de prueba de inglés a español."
            else:
                return f"Texto traducido de {idioma_origen} a {idioma_destino}"
            
        except Exception as e:
            print(f"Error en la traducción: {str(e)}")
            return None