# -*- coding: utf-8 -*-
"""app2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GknAUkeNS_hlrCbkbDO0F6_1uc2KRy7R
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pytesseract
from gtts import gTTS
import os
import glob
import time

# Define la función text_to_speech
def text_to_speech(text, tld):
    tts = gTTS(text, lang=tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name

# Barra lateral con opciones
with st.sidebar:
    filtro = st.radio("Aplicar Filtro", ('Con Filtro', 'Sin Filtro'))

# Cargar la imagen
img_file_buffer = st.file_uploader("Cargar imagen", type=["jpg", "png", "jpeg"])
if img_file_buffer is not None:
    bytes_data = img_file_buffer.read()
    image = Image.open(img_file_buffer)
    st.image(image, caption="Imagen cargada", use_column_width=True)

    # Convertir la imagen en texto utilizando pytesseract
    cv2_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    if filtro == 'Con Filtro':
        cv2_img = cv2.bitwise_not(cv2_img)
    text = pytesseract.image_to_string(cv2_img)
    st.write(text)

tld="es"

# Botón para convertir texto en audio
if st.button("Convertir a audio"):
    if text:
        result = text_to_speech(text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
        st.markdown(f"## Texto en audio:")
        st.write(f"{text}")

# Función para eliminar archivos antiguos
def remove_files(n):
    mp3_files = glob.glob("temp/*.mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)
