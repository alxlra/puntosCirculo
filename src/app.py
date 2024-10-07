# app.py
import streamlit as st
from preferencias import leer_preferencias


st.title("🤖 Tripteron")
st.write("Selecciona del menú de la izquierda el tipo de movimiento que deseas para generar los puntos.")
st.write("Comienza con la configuración de los límites de trabajo.")

# Leer y mostrar las preferencias guardadas
preferencias = leer_preferencias()
if not preferencias:
    st.error("No hay preferencias guardadas.", icon="ℹ")
else:
    st.success("Archivo de preferencias configurado", icon="✔")
    st.json(preferencias)