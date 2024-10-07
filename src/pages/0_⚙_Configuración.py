import streamlit as st
import pandas as pd
import json
from preferencias import guardar_preferencias

st.title("⚙ Configuración de Tripteron")
st.subheader("Limites de trabajo")
col1,col2 = st.columns(2)
with col1:
    x_min = st.number_input("Límite mínimo X:", min_value=0.0, max_value=30.0, value=8.125, format="%.3f", step=0.5)
    y_min = st.number_input("Límite mínimo Y:", min_value=0.0, max_value=30.0, value=8.125, format="%.3f", step=0.5)
    z_min = st.number_input("Límite mínimo Z:", min_value=0.0, max_value=30.0, value=5.625, format="%.3f", step=0.5)
with col2:
    x_max = st.number_input("Límite máximo X:", min_value=0.0, max_value=40.0, value=35.625, format="%.3f", step=0.5)
    y_max = st.number_input("Límite máximo Y:", min_value=0.0, max_value=30.0, value=21.75, format="%.3f", step=0.5)
    #center_z = st.number_input("Límite máximo Z:", min_value=2.0, max_value=30.0, value=5.625, format="%.3f", step=0.5)
#z_max = z_min+1
st.divider()
st.subheader("Posiciones de carros")
ini_a = st.number_input("Offset carro A:", min_value=0.0, max_value=30.0, value=0.0, format="%.3f")
ini_b = st.number_input("Offset carro B:", min_value=0.0, max_value=30.0, value=16.25, format="%.3f")
ini_c = st.number_input("Offset carro C:", min_value=0.0, max_value=30.0, value=2.5, format="%.3f")

if st.button("💾 Guardar preferencias"):
    preferencias = {
        'x_min': x_min, 'y_min': y_min, 'z_min': z_min,
        'x_max': x_max, 'y_max': y_max,
        'ini_a': ini_a, 'ini_b': ini_b, 'ini_c': ini_c
    }
    
    # Guardar las preferencias en un archivo JSON
    guardar_preferencias(preferencias)
    
    st.success("Preferencias guardadas", icon="✔")