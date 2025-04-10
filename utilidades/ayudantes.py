## Elisanna María Martínez Sánchez
## 23-EISN-2-074

"""
Funciones auxiliares para la aplicación
"""

import time
import os
import datetime
from configuracion import IDIOMAS_SOPORTADOS

def obtener_codigo_idioma(nombre_idioma):
    """
    Obtiene el código del idioma a partir de su nombre.
    """
    if not nombre_idioma:
        return None
        
    return IDIOMAS_SOPORTADOS.get(nombre_idioma.lower(), None)

def obtener_nombre_idioma(codigo_idioma):
    """
    Obtiene el nombre del idioma a partir de su código.
    """
    for nombre, codigo in IDIOMAS_SOPORTADOS.items():
        if codigo == codigo_idioma:
            return nombre
    return None

def limpiar_archivos_viejos(directorio, antiguedad_maxima_horas=1):
    """
    Limpia archivos temporales antiguos.
    """
    if not os.path.exists(directorio):
        return 0
    
    tiempo_actual = time.time()
    antiguedad_maxima_segundos = antiguedad_maxima_horas * 3600
    archivos_eliminados = 0
    
    for nombre_archivo in os.listdir(directorio):
        ruta_archivo = os.path.join(directorio, nombre_archivo)
        if os.path.isfile(ruta_archivo):
            antiguedad_archivo = tiempo_actual - os.path.getmtime(ruta_archivo)
            if antiguedad_archivo > antiguedad_maxima_segundos:
                try:
                    os.remove(ruta_archivo)
                    archivos_eliminados += 1
                    print(f"Archivo eliminado: {ruta_archivo}")
                except Exception as e:
                    print(f"Error al eliminar {ruta_archivo}: {e}")
    
    return archivos_eliminados

def formatear_marca_tiempo(marca_tiempo):
    """
    Formatea una marca de tiempo a un formato legible.
     
    """
    return datetime.datetime.fromtimestamp(marca_tiempo).strftime("%H:%M:%S")