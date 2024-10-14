import streamlit as st
import pandas as pd
import json
from preferencias import *

# Leer y mostrar las preferencias guardadas
preferencias = leer_preferencias()
if not preferencias:
    st.error("No hay preferencias guardadas.", icon="ℹ")
ini_a = preferencias.get("ini_a", 0.0)
ini_b = preferencias.get("ini_b", 16.25)
ini_c = preferencias.get("ini_c", 2.5)
center_z = preferencias.get("z_min", 5.625)
x_min = preferencias.get("x_min", 0.0)
x_max = preferencias.get("x_max", 35.0)
y_min = preferencias.get("y_min", 0.0)
y_max = preferencias.get("y_max", 35.0)
ini_x = preferencias.get("ini_x", 8.125)
ini_y = preferencias.get("ini_y", 8.125)
ini_z = preferencias.get("ini_z", 5.625)

st.title("⚙ Configuración de Tripteron")
st.subheader("Limites de trabajo")
col1,col2 = st.columns(2)
with col1:
    x_min = st.number_input("Límite mínimo X:", value=preferencias.get("x_min", 0), format="%.3f", step=0.5)
    y_min = st.number_input("Límite mínimo Y:", value=preferencias.get("y_min", 0), format="%.3f", step=0.5)
    z_min = st.number_input("Límite mínimo Z:", value=preferencias.get("z_min", 0), format="%.3f", step=0.5)
with col2:
    x_max = st.number_input("Límite máximo X:", min_value=0.0, max_value=40.0, value=preferencias.get("x_max", 35.625), format="%.3f", step=0.5)
    y_max = st.number_input("Límite máximo Y:", min_value=0.0, max_value=30.0, value=preferencias.get("y_max", 21.75), format="%.3f", step=0.5)

escala = st.number_input("Un movimiento de carro equivale a:", min_value=0.1, max_value=10.0, value=preferencias.get("escala", 0.2), format="%.3f", step=0.1)
st.divider()
st.subheader("Coordenadas iniciales", help="Coordenadas origen de la punta")

col1,col2,col3 = st.columns(3)
with col1:
    ini_x = st.number_input("X inicial:", min_value=0.0, max_value=30.0, value=preferencias.get("ini_x", 8.125), format="%.3f")
with col2:
    ini_y = st.number_input("Y inicial:", min_value=0.0, max_value=30.0, value=preferencias.get("ini_y", 8.125), format="%.3f")
with col3:
    ini_z = st.number_input("Z inicial:", min_value=-10.0, max_value=10.0, value=preferencias.get("ini_z", 5.625), format="%.3f")

st.divider()
st.subheader("Posiciones de carros 👼", help="Orden: [B] &nbsp;&nbsp; [C] [A]")

col1,col2,col3 = st.columns(3)
with col1:
    ini_b = st.number_input("Offset carro B:", min_value=0.0, max_value=30.0, value=preferencias.get("ini_b", 16.25), format="%.3f", help="Carro izquierda independiente")
with col2:
    ini_c = st.number_input("Offset carro C:", min_value=0.0, max_value=30.0, value=preferencias.get("ini_c", 2.5), format="%.3f", help="Carro central")
with col3:
    ini_a = st.number_input("Offset carro A:", min_value=0.0, max_value=30.0, value=preferencias.get("ini_a", 0.0), format="%.3f", help="Carro derecha")

if st.button("💾 Guardar preferencias"):
    preferencias = {
        'x_min': x_min, 'y_min': y_min, 'z_min': z_min,
        'x_max': x_max, 'y_max': y_max,
        'ini_a': ini_a, 'ini_b': ini_b, 'ini_c': ini_c,
        'ini_x': ini_x, 'ini_y': ini_y, 'ini_z': ini_z,
        'escala': escala
    }
    
    # Guardar las preferencias en un archivo JSON
    guardar_preferencias(preferencias)
    
    st.success("Preferencias guardadas", icon="✔")