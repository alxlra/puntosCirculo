# app.py
import streamlit as st
from preferencias import leer_preferencias


st.title("🤖 Tripteron")
st.write("Bienvenido al generador de puntos para el Tripteron. Esta aplicación permite generar los puntos necesarios para poder dibujar en 2D.")
st.write("Selecciona del menú de la izquierda el tipo de movimiento que deseas para generar los puntos. Comienza con la configuración de los límites de trabajo.")

# Leer y mostrar las preferencias guardadas
preferencias = leer_preferencias()
if not preferencias:
    st.error("No hay preferencias guardadas.", icon="ℹ")
else:
    st.success("Se encontró un archivo de preferencias", icon="✔")
    st.json(preferencias)

st.image("src/img/robot.jpg", use_column_width=True)