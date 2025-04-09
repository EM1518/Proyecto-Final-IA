## Elisanna María Martínez Sánchez
## 23-EISN-2-074

"""
Aplicación principal del intérprete 
"""

from configuracion import CLAVE_API_OPENAI
from componentes.reconocimiento_voz import ReconocedorVoz
from componentes.traduccion import Traductor
from componentes.texto_a_voz import TextoAVoz

def main():
    """
    Función principal de la aplicación.
    """
    print("Inicializando aplicación...")
    
    # Verificar configuración
    if not CLAVE_API_OPENAI:
        print("ADVERTENCIA: No se ha configurado OPENAI_API_KEY")
        print("Por favor, crea un archivo .env con tu clave API.")
    else:
        print("Configuración cargada correctamente.")
    
    # Inicializar los componentes
    reconocedor = ReconocedorVoz()
    print("Reconocedor de voz inicializado.")

    traductor = Traductor()
    print("Traductor inicializado.")

    convertidor = TextoAVoz()
    print("Convertidor de texto a voz inicializado.")

    # Ejemplo de uso 
    texto_ejemplo = "Texto de prueba para reconocimiento de voz."
    texto_traducido = traductor.traducir(texto_ejemplo, "español", "inglés")
    print(f"Ejemplo de traducción: '{texto_ejemplo}' -> '{texto_traducido}'")
    
    # Ejemplo de conversión a voz
    ruta_audio = convertidor.texto_a_voz(texto_traducido, "en")
    if ruta_audio:
        print(f"Audio generado en: {ruta_audio}")

if __name__ == "__main__":
    main()