## Elisanna María Martínez Sánchez
## 23-EISN-2-074

"""
Aplicación principal del intérprete 
"""

from configuracion import CLAVE_API_OPENAI

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
    
    print("Configuración inicial completa.")

if __name__ == "__main__":
    main()