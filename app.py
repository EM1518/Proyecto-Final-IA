## Elisanna María Martínez Sánchez
## 23-EISN-2-074

"""
Aplicación principal del intérprete 
"""
import gradio as gr
import os
import time
from configuracion import CLAVE_API_OPENAI, DIRECTORIO_AUDIO, IDIOMAS_SOPORTADOS
from componentes.reconocimiento_voz import ReconocedorVoz
from componentes.traduccion import Traductor
from componentes.texto_a_voz import TextoAVoz
from utilidades.ayudantes import obtener_codigo_idioma, limpiar_archivos_viejos, formatear_marca_tiempo

# Verificar que la clave API esté configurada
if not CLAVE_API_OPENAI:
    print("No se ha configurado la clave API de OpenAI. Por favor, crea un archivo .env con tu clave.")

# Inicializar los componentes
reconocedor_voz = ReconocedorVoz()
traductor = Traductor()
texto_a_voz = TextoAVoz()

# CSS para mejorar diseño inicial
css = """
.contenedor {
    margin: 0 auto;
    max-width: 800px;
}

.titulo {
    text-align: center;
    margin-bottom: 20px;
}

.seccion-hablante {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 10px;
}

.procesando {
    display: inline-block;
    margin-left: 10px;
    animation: pulso 1.5s infinite;
}

@keyframes pulso {
    0% { opacity: 0.5; }
    50% { opacity: 1; }
    100% { opacity: 0.5; }
}

.registro-hora {
    color: #888;
    font-size: 0.8em;
    margin-top: 5px;
}
"""

def procesar_audio1(audio, idioma_origen, idioma_destino):
    """
    Procesa el audio grabado por el Hablante 1.
    """
    if audio is None:
        return "No se ha grabado audio.", "No hay texto para traducir.", None

    # Registrar la hora de inicio
    hora_inicio = time.time()
    hora_inicio_str = formatear_marca_tiempo(hora_inicio)

    # Obtener códigos de idioma
    codigo_origen = obtener_codigo_idioma(idioma_origen)
    codigo_destino = obtener_codigo_idioma(idioma_destino)

    # Transcribir el audio
    print(f"[{hora_inicio_str}] Transcribiendo audio del Hablante 1...")
    texto_original = reconocedor_voz.reconocer_voz_desde_archivo(audio, codigo_origen)
    
    if not texto_original:
        return f"No se pudo transcribir el audio ({hora_inicio_str}).", "Error en la transcripción.", None
    
    # Traducir el texto
    print(f"[{hora_inicio_str}] Traduciendo texto de {idioma_origen} a {idioma_destino}...")
    texto_traducido = traductor.traducir(texto_original, idioma_origen, idioma_destino)
    
    if not texto_traducido:
        return f"{texto_original} ({hora_inicio_str})", "Error en la traducción.", None
    
    # Convertir el texto traducido a voz
    print(f"[{hora_inicio_str}] Generando audio en {idioma_destino}...")
    archivo_audio = texto_a_voz.texto_a_voz(texto_traducido, codigo_destino)
    
    # Registrar la hora de finalización
    hora_fin = time.time()
    duracion = round(hora_fin - hora_inicio, 2)
    print(f"Procesamiento completado en {duracion} segundos.")
    
    # Agregar marca de tiempo a los resultados
    texto_original_con_hora = f"{texto_original}\n\n<div class='registro-hora'>Procesado en {duracion}s - {hora_inicio_str}</div>"
    
    return texto_original_con_hora, texto_traducido, archivo_audio


def procesar_audio2(audio, idioma_origen, idioma_destino):
    """
    Procesa el audio grabado por el Hablante 2 (intercambiando los idiomas).
    """
    if audio is None:
        return "No se ha grabado audio.", "No hay texto para traducir.", None
    
    # Registrar la hora de inicio
    hora_inicio = time.time()
    hora_inicio_str = formatear_marca_tiempo(hora_inicio)

    # Para el Hablante 2, los idiomas se invierten
    codigo_destino = obtener_codigo_idioma(idioma_origen)
    codigo_origen = obtener_codigo_idioma(idioma_destino)
    
    # Transcribir el audio
    print(f"[{hora_inicio_str}] Transcribiendo audio del Hablante 2...")
    texto_original = reconocedor_voz.reconocer_voz_desde_archivo(audio, codigo_origen)
    
    if not texto_original:
        return f"No se pudo transcribir el audio ({hora_inicio_str}).", "Error en la transcripción.", None
    
    # Traducir el texto
    print(f"[{hora_inicio_str}] Traduciendo texto de {idioma_destino} a {idioma_origen}...")
    texto_traducido = traductor.traducir(texto_original, idioma_destino, idioma_origen)
    
    if not texto_traducido:
        return f"{texto_original} ({hora_inicio_str})", "Error en la traducción.", None
    
    # Convertir el texto traducido a voz
    print(f"[{hora_inicio_str}] Generando audio en {idioma_origen}...")
    archivo_audio = texto_a_voz.texto_a_voz(texto_traducido, codigo_destino)
    
    # Registrar la hora de finalización
    hora_fin = time.time()
    duracion = round(hora_fin - hora_inicio, 2)
    print(f"Procesamiento completado en {duracion} segundos.")
    
    # Agregar marca de tiempo a los resultados
    texto_original_con_hora = f"{texto_original}\n\n<div class='registro-hora'>Procesado en {duracion}s - {hora_inicio_str}</div>"
    
    return texto_original_con_hora, texto_traducido, archivo_audio

# Definir la interfaz de Gradio
with gr.Blocks(title="Intérprete en Tiempo Real", css=css) as demo:
    gr.HTML("""
        <div class="titulo">
            <h1>🌎 Intérprete en Tiempo Real</h1>
            <p>Esta aplicación te permite comunicarte con personas que hablan diferentes idiomas
            a través de reconocimiento de voz, traducción automática y síntesis de voz.</p>
        </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            idioma_origen = gr.Dropdown(
                choices=list(IDIOMAS_SOPORTADOS.keys()),
                value="español",
                label="Idioma de origen"
            )
        with gr.Column(scale=1):
            idioma_destino = gr.Dropdown(
                choices=list(IDIOMAS_SOPORTADOS.keys()),
                value="inglés",
                label="Idioma de destino"
            )
    
    with gr.Row():
        with gr.Column():
            # Sección para Hablante 1
            with gr.Group(elem_classes=["seccion-hablante"]):
                gr.Markdown("### 🎤 Hablante 1")
                entrada_audio1 = gr.Audio(
                    sources=["microphone"],
                    type="filepath",
                    label="Grabación (en tu idioma)"
                )
                boton_traducir1 = gr.Button("Traducir y Enviar")
                
                with gr.Row():
                    texto_original1 = gr.HTML(label="Texto original")
                    texto_traducido1 = gr.HTML(label="Texto traducido")
                
                salida_audio1 = gr.Audio(label="Audio traducido", autoplay=True)
        
        with gr.Column():
            # Sección para Hablante 2
            with gr.Group(elem_classes=["seccion-hablante"]):
                gr.Markdown("### 🎤 Hablante 2")
                entrada_audio2 = gr.Audio(
                    sources=["microphone"],
                    type="filepath",
                    label="Grabación (en el otro idioma)"
                )
                boton_traducir2 = gr.Button("Traducir y Enviar")
                
                with gr.Row():
                    texto_original2 = gr.HTML(label="Texto original")
                    texto_traducido2 = gr.HTML(label="Texto traducido")
                
                salida_audio2 = gr.Audio(label="Audio traducido", autoplay=True)
    
    # Configurar eventos
    boton_traducir1.click(
        fn=procesar_audio1,
        inputs=[entrada_audio1, idioma_origen, idioma_destino],
        outputs=[texto_original1, texto_traducido1, salida_audio1]
    )
    
    boton_traducir2.click(
        fn=procesar_audio2,
        inputs=[entrada_audio2, idioma_origen, idioma_destino],
        outputs=[texto_original2, texto_traducido2, salida_audio2]
    )
    
    # Instrucciones 
    with gr.Accordion("Instrucciones de uso", open=False):
        gr.Markdown("""
        ## Cómo usar esta aplicación
        
        1. **Configuración inicial**:
           - Selecciona los idiomas de origen y destino en la parte superior
        
        2. **Para hablar como Hablante 1**:
           - Haz clic en el botón de micrófono en el panel izquierdo
           - Habla claramente en tu idioma nativo
           - Presiona "Detener" cuando termines
           - Haz clic en "Traducir y Enviar" para procesar el audio
        
        3. **Para hablar como Hablante 2**:
           - Haz clic en el botón de micrófono en el panel derecho
           - Habla claramente en el otro idioma
           - Presiona "Detener" cuando termines
           - Haz clic en "Traducir y Enviar" para procesar el audio
        
        4. **Interpretación**:
           - El texto original se mostrará en la primera columna
           - La traducción aparecerá en la segunda columna
           - El audio traducido se reproducirá automáticamente
        """)

# Lanzar la aplicación
if __name__ == "__main__":
    # Limpiar archivos temporales antes de iniciar
    limpiar_archivos_viejos(DIRECTORIO_AUDIO)

    # Lanzar la interfaz
    demo.launch(share=False)