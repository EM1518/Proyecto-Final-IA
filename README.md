# Proyecto-de-Final-IA
## Elisanna María Martínez Sánchez
## 23-EISN-2-074
## Intérprete en tiempo real

Esta aplicación permite la comunicación entre personas que hablan diferentes idiomas mediante traducción de voz en tiempo real.

### Instrucciones de instalación y ejecución

1. Clona este repositorio
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Crea un archivo `.env` en la raíz del proyecto con tu clave API de OpenAI:
```
OPENAI_API_KEY=tu_clave_api_aqui
```

4. Ejecuta la aplicación:
```bash
python app.py
```

5. Abre tu navegador web en la dirección que muestra la terminal (generalmente http://127.0.0.1:7860)

### Uso básico

1. Selecciona los idiomas de origen y destino
2. Usa los botones de micrófono para grabar tu mensaje
3. Presiona "Traducir y Enviar"
4. La traducción aparecerá en la ventana de chat y se reproducirá automáticamente

### Tecnologías utilizadas

- OpenAI Whisper API (reconocimiento de voz)
- OpenAI GPT API (traducción)
- gTTS (conversión de texto a voz)
- Gradio (interfaz de usuario)