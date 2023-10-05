from textblob import TextBlob
import pandas as pd
import streamlit as st
from googletrans import Translator
import os
import time
import glob
from gtts import gTTS
from PIL import Image

# Inicialización del traductor de Google y título de la aplicación
translator = Translator()
st.title("Voz y Emoción: Convierte Texto en Audio.")

# Imagen debajo del título
image = st.image("medidor.jpg", use_container_width=True)

# Crear un directorio temporal si no existe
try:
    os.mkdir("temp")
except:
    pass

# Encabezado y descripción de la funcionalidad de la aplicación
st.subheader("Texto a audio.")
st.write("""
La aplicación 'Voz y Emoción: Convierte Texto en Audio.' te permite convertir texto en archivos de audio de manera rápida y sencilla. Además de esta funcionalidad, la aplicación también es capaz de analizar el sentimiento del texto ingresado, proporcionando una comprensión instantánea de las emociones expresadas en el contenido. Facilita la accesibilidad, la comunicación natural y la interacción inclusiva, lo que la hace ideal tanto para usuarios con discapacidades visuales como para aquellos que desean explorar el análisis de sentimientos en sus textos. ¡Convierte tus palabras en voz y descubre las emociones detrás de cada mensaje!
""")
           
# Entrada de texto del usuario
text = st.text_input("Ingrese el texto.")

# Idioma predeterminado
tld = "es"

def text_to_speech(text, tld):
    # Convierte el texto en voz y guarda el archivo MP3 en el directorio "temp"
    tts = gTTS(text, "es", tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

if st.button("Convertir y Analizar"):
    # Genera el audio y muestra el análisis de sentimientos
    result, output_text = text_to_speech(text, tld)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown(f"## Tu audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)
    
    translation = translator.translate(text, src="es", dest="en")
    trans_text = translation.text
    blob = TextBlob(trans_text)
    st.markdown(f"## Sentimientos Detectados:")
    st.write('Polarity: ', round(blob.sentiment.polarity,2))
    st.write('Subjectivity: ', round(blob.sentiment.subjectivity,2))
    x = round(blob.sentiment.polarity,2)
    if x >= 0.5:
        st.write( 'Es un sentimiento Positivo 😊')
    elif x <= -0.5:
        st.write( 'Es un sentimiento Negativo 😔')
    else:
        st.write( 'Es un sentimiento Neutral 😐')

def remove_files(n):
    # Elimina archivos MP3 más antiguos en el directorio "temp"
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)
