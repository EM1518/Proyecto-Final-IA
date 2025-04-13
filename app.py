## Elisanna María Martínez Sánchez
## 23-EISN-2-074

"""
Aplicación principal del intérprete 
"""
import gradio as gr
import os
import time
import random
import tempfile
import shutil
from configuracion import CLAVE_API_OPENAI, DIRECTORIO_AUDIO, IDIOMAS_SOPORTADOS
from componentes.reconocimiento_voz import ReconocedorVoz
from componentes.traduccion import Traductor
from componentes.texto_a_voz import TextoAVoz
from utilidades.ayudantes import obtener_codigo_idioma, limpiar_archivos_viejos

# Verificar que la clave API esté configurada
if not CLAVE_API_OPENAI:
    print("No se ha configurado la clave API de OpenAI. Por favor, crea un archivo .env con tu clave.")

# Inicializar los componentes
reconocedor_voz = ReconocedorVoz()
traductor = Traductor()
texto_a_voz = TextoAVoz()

# Historial de conversación
historial_conversacion = []

# CSS para mejorar diseño inicial
css = """
.conversation-container {
    max-height: 600px;
    overflow-y: auto;
    border-radius: 10px;
    background: #1a1c24;
    padding: 15px;
    margin-bottom: 20px;
}

.message {
    display: flex;
    margin-bottom: 20px;
    animation: fadeIn 0.5s;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.message-left {
    justify-content: flex-start;
}

.message-right {
    justify-content: flex-end;
}

.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin: 5px 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: white;
}

.avatar-1 {
    background: linear-gradient(135deg, #3498db, #2980b9);
}

.avatar-2 {
    background: linear-gradient(135deg, #2ecc71, #27ae60);
}

.bubble {
    padding: 12px 15px;
    border-radius: 18px;
    max-width: 70%;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.bubble-left {
    background: linear-gradient(135deg, #3498db, #2574a9);
    color: white;
    border-top-left-radius: 2px;
}

.bubble-right {
    background: linear-gradient(135deg, #2ecc71, #27ae60);
    color: white;
    border-top-right-radius: 2px;
}

.translated-text {
    font-size: 14px;
    opacity: 0.9;
    margin-top: 5px;
    padding-top: 5px;
    border-top: 1px solid rgba(255,255,255,0.2);
}

.controls {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 20px;
}

.speaker-button {
    padding: 15px 25px;
    border-radius: 10px;
    border: none;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.speaker-1 {
    background: linear-gradient(135deg, #3498db, #2980b9);
    color: white;
}

.speaker-2 {
    background: linear-gradient(135deg, #2ecc71, #27ae60);
    color: white;
}

.speaker-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.speaker-button:active {
    transform: translateY(0);
}

.processing {
    display: inline-block;
    margin-left: 10px;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% { opacity: 0.5; }
    50% { opacity: 1; }
    100% { opacity: 0.5; }
}

.speaker-container {
    border: 1px solid rgba(100, 100, 100, 0.3);
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 10px;
}
"""

def procesar_audio1(audio, idioma_origen, idioma_destino, chatbox):
    """
    Procesa el audio grabado por el Hablante 1.
    """
    # Si no hay audio, retornar sin cambios
    if audio is None:
        return chatbox, None, None

    # Obtener códigos de idioma
    codigo_origen = obtener_codigo_idioma(idioma_origen)
    codigo_destino = obtener_codigo_idioma(idioma_destino)

    # Transcribir el audio
    texto_original = reconocedor_voz.reconocer_voz_desde_archivo(audio, codigo_origen)
    
    if not texto_original:
        return chatbox + f"\n\n❌ **Error**: No se pudo transcribir el audio. Por favor, habla claramente.", None, None
    
    # Traducir el texto
    texto_traducido = traductor.traducir(texto_original, idioma_origen, idioma_destino)
    
    if not texto_traducido:
        return chatbox + f"\n\n❌ **Error**: No se pudo traducir el texto. Inténtalo de nuevo.", None, None
    
    # Convertir el texto traducido a voz
    archivo_audio = texto_a_voz.texto_a_voz(texto_traducido, codigo_destino)
    
    # Copiar el archivo de audio a una ubicación permanente
    ruta_permanente = os.path.join(DIRECTORIO_AUDIO, f"audio_{int(time.time())}_{random.randint(1000, 9999)}.mp3")
    shutil.copy2(archivo_audio, ruta_permanente)
    
    # Guardar en el historial
    historial_conversacion.append({
        "hablante": "Hablante 1",
        "avatar": "1",
        "texto_original": texto_original,
        "texto_traducido": texto_traducido,
        "idioma_origen": idioma_origen,
        "idioma_destino": idioma_destino,
        "ruta_audio": ruta_permanente,
        "timestamp": time.time()
    })
    
    # Actualizar el chatbox con formato HTML personalizado
    chat_actualizado = crear_html_chat()
    
    # Retornar el chat actualizado, el audio para reproducción automática y None para limpiar el componente de audio
    return chat_actualizado, archivo_audio, None


def procesar_audio2(audio, idioma_origen, idioma_destino, chatbox):
    """
    Procesa el audio grabado por el Hablante 2 (intercambiando los idiomas).
    """
    # Si no hay audio, retornar sin cambios
    if audio is None:
        return chatbox, None, None
    
    # Para el Hablante 2, los idiomas se invierten
    codigo_destino = obtener_codigo_idioma(idioma_origen)
    codigo_origen = obtener_codigo_idioma(idioma_destino)
    
    # Transcribir el audio
    texto_original = reconocedor_voz.reconocer_voz_desde_archivo(audio, codigo_origen)
    
    if not texto_original:
        return chatbox + f"\n\n❌ **Error**: No se pudo transcribir el audio. Por favor, habla claramente.", None, None
    
    # Traducir el texto
    texto_traducido = traductor.traducir(texto_original, idioma_destino, idioma_origen)
    
    if not texto_traducido:
        return chatbox + f"\n\n❌ **Error**: No se pudo traducir el texto. Inténtalo de nuevo.", None, None
    
    # Convertir el texto traducido a voz
    archivo_audio = texto_a_voz.texto_a_voz(texto_traducido, codigo_destino)
    
    # Copiar el archivo de audio a una ubicación permanente
    ruta_permanente = os.path.join(DIRECTORIO_AUDIO, f"audio_{int(time.time())}_{random.randint(1000, 9999)}.mp3")
    shutil.copy2(archivo_audio, ruta_permanente)
    
    # Guardar en el historial
    historial_conversacion.append({
        "hablante": "Hablante 2",
        "avatar": "2",
        "texto_original": texto_original,
        "texto_traducido": texto_traducido,
        "idioma_origen": idioma_destino,  # Invertido
        "idioma_destino": idioma_origen,  # Invertido
        "ruta_audio": ruta_permanente,
        "timestamp": time.time()
    })
    
    # Actualizar el chatbox con formato HTML personalizado
    chat_actualizado = crear_html_chat()
    
    # Retornar el chat actualizado, el audio para reproducción automática y None para limpiar el componente de audio
    return chat_actualizado, archivo_audio, None


def crear_html_chat():
    """
    Crea el HTML para la vista de chat basado en el historial de conversación.
    """
    if not historial_conversacion:
        return "<div class='conversation-container'><p style='text-align: center; color: #888;'>La conversación aparecerá aquí. Comienza grabando un mensaje.</p></div>"
    
    chat_html = "<div class='conversation-container'>"
    
    for idx, entrada in enumerate(historial_conversacion):
        hablante = entrada["hablante"]
        avatar = entrada["avatar"]
        texto_traducido = entrada["texto_traducido"]
        
        # Crear burbuja de chat con alineación adecuada
        if avatar == "1":
            alineacion = "left"
        else:
            alineacion = "right"
        
        chat_html += f"""
        <div class='message message-{alineacion}'>
            <div class='avatar avatar-{avatar}'>{avatar}</div>
            <div class='bubble bubble-{alineacion}'>
                <div style='display: flex; align-items: center;'>
                    <span>{hablante}</span>
                </div>
                <div class='translated-text'>{texto_traducido}</div>
            </div>
        </div>
        """
    
    chat_html += "</div>"
    return chat_html

def limpiar_conversacion():
    """
    Limpia el historial de conversación.
    """
    historial_conversacion.clear()
    return crear_html_chat(), None, None, None

# Definir la interfaz de Gradio
with gr.Blocks(title="Intérprete en Tiempo Real", theme=gr.themes.Soft(), css=css) as demo:
    gr.HTML("""
        <div style="text-align: center; margin-bottom: 10px;">
            <h1 style="margin-bottom: 10px;">🌎 Intérprete en Tiempo Real</h1>
            <p>Esta aplicación te permite comunicarte con personas que hablan diferentes idiomas.
            Habla en tu idioma, y la aplicación traducirá y reproducirá tu mensaje en el idioma seleccionado.</p>
        </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            idioma_origen = gr.Dropdown(
                choices=list(IDIOMAS_SOPORTADOS.keys()),
                value="español",
                label="Idioma de origen",
                container=True
            )
        with gr.Column(scale=1):
            idioma_destino = gr.Dropdown(
                choices=list(IDIOMAS_SOPORTADOS.keys()),
                value="inglés",
                label="Idioma de destino",
                container=True
            )
    
        # Área de chat
    visualizacion_chat = gr.HTML(crear_html_chat())
    
    # Audio para reproducción automática
    audio_reproduccion = gr.Audio(label="", visible=False, autoplay=True)

    with gr.Row():
        with gr.Column():
            # Sección para Hablante 1
            gr.Markdown("### 🎤 Hablante 1", elem_classes=["speaker-container"])
            entrada_audio1 = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="Grabación (en tu idioma)"
            )
            boton_traducir1 = gr.Button("Traducir y Enviar", variant="primary", elem_classes=["speaker-button", "speaker-1"])
        
        with gr.Column():
            # Sección para Hablante 2
            gr.Markdown("### 🎤 Hablante 2", elem_classes=["speaker-container"])
            entrada_audio2 = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="Grabación (en el otro idioma)"
            )
            boton_traducir2 = gr.Button("Traducir y Enviar", variant="primary", elem_classes=["speaker-button", "speaker-2"])
    
    with gr.Row():
        boton_limpiar = gr.Button("🗑️ Borrar Conversación")
    
    # Configurar eventos
    boton_traducir1.click(
        fn=procesar_audio1,
        inputs=[entrada_audio1, idioma_origen, idioma_destino, visualizacion_chat],
        outputs=[visualizacion_chat, audio_reproduccion, entrada_audio1],
        queue=False
    )
    
    boton_traducir2.click(
        fn=procesar_audio2,
        inputs=[entrada_audio2, idioma_origen, idioma_destino, visualizacion_chat],
        outputs=[visualizacion_chat, audio_reproduccion, entrada_audio2],
        queue=False
    )
    
    boton_limpiar.click(
        fn=limpiar_conversacion,
        inputs=[],
        outputs=[visualizacion_chat, audio_reproduccion, entrada_audio1, entrada_audio2]
    )
    
    # Instrucciones
    with gr.Accordion("Instrucciones de uso", open=False):
        gr.Markdown("""
        ## Cómo usar esta aplicación
        
        1. Selecciona los idiomas de origen y destino en la parte superior
        
        2. Para hablar como Hablante 1:
           - Haz clic en el botón de micrófono en el panel izquierdo
           - Habla claramente en tu idioma nativo
           - Presiona "Detener" cuando termines
           - Haz clic en "Traducir y Enviar" para procesar
        
        3. Para hablar como Hablante 2:
           - Haz clic en el botón de micrófono en el panel derecho
           - Habla claramente en el otro idioma
           - Presiona "Detener" cuando termines
           - Haz clic en "Traducir y Enviar" para procesar
        
        4. La traducción se mostrará en la ventana de chat y se reproducirá automáticamente
        
        5. Puedes borrar la conversación en cualquier momento con el botón "Borrar Conversación"
        """)

# Lanzar la aplicación
if __name__ == "__main__":
    # Limpiar archivos temporales antes de iniciar
    limpiar_archivos_viejos(DIRECTORIO_AUDIO)
    
    # Lanzar la interfaz
    demo.launch(share=False)