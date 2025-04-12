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
            
            # Preparar el mensaje para la API
            prompt = f"""Traduce el siguiente texto de {idioma_origen} a {idioma_destino}.
                       Por favor, proporciona solo la traducción sin explicaciones ni texto adicional:
                       
                       "{texto}"
                       """
            
            # Llamar a la API de OpenAI
            respuesta = openai.chat.completions.create(
                model=self.modelo,
                messages=[
                    {"role": "system", "content": "Eres un traductor preciso y eficiente. Proporciona solo la traducción solicitada sin ningún texto adicional."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Menor temperatura para traducciones más precisas
                max_tokens=1024
            )
            
            # Extraer y devolver el texto traducido
            texto_traducido = respuesta.choices[0].message.content.strip()
            
            # Eliminar comillas si el modelo las incluye
            if texto_traducido.startswith('"') and texto_traducido.endswith('"'):
                texto_traducido = texto_traducido[1:-1]
                
            return texto_traducido
            
        except Exception as e:
            print(f"Error en la traducción: {str(e)}")
            return None