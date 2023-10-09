# -*- coding: utf-8 -*-
"""app2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GknAUkeNS_hlrCbkbDO0F6_1uc2KRy7R
"""

import streamlit as st
import os
import time
import glob
import os
from gtts import gTTS
from PIL import Image
import cv2
import numpy as np
import pytesseract
from PIL import Image

st.title("Reconocimiento óptico de Caracteres")

img_file_buffer = st.file_uploader("Cargar imagen", type=["jpg", "png", "jpeg"])

with st.sidebar:
    filtro = st.radio("Aplicar Filtro", ('Con Filtro', 'Sin Filtro'))

if img_file_buffer is not None:
    # Leer la imagen
    bytes_data = img_file_buffer.read()
    image = Image.open(img_file_buffer)
    st.image(image, caption="Imagen cargada", use_column_width=True)

    # Convertir la imagen en texto utilizando pytesseract
    cv2_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    if filtro == 'Con Filtro':
        cv2_img = cv2.bitwise_not(cv2_img)
    text = pytesseract.image_to_string(cv2_img)

    # Mostrar el texto extraído
    st.write("Texto extraído de la imagen:")
    st.write(text)

    # Crear un botón para convertir el texto en audio
    if st.button("Convertir a audio"):
        if text:
            tts = gTTS(text, lang='es', slow=False)  # Cambia 'es' al idioma que desees
            audio_bytes = tts.get_audio_data()
            st.audio(audio_bytes, format="audio/mpeg", start_time=0)