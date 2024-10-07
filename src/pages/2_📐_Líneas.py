import streamlit as st
import math
import pandas as pd
from matplotlib import pyplot as plt

from preferencias import leer_preferencias

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
z_min = preferencias.get("z_min", 0.0)

if not preferencias:
    st.error("No hay preferencias guardadas.", icon="ℹ")

def calcular_lineas(y_start, y_end, z, lineas):
    df = pd.DataFrame(columns=["X", "Y", "Z"])
    y = (y_end - y_start)/(lineas+1)
    for i in range(lineas):
        x = calcula_x(y)
        df.loc[len(df)] = [x, y, center_z]
        
    return df


st.title("📐 Generador de líneas")

col1,col2 = st.columns(2)
with col1:
    y_start = st.number_input("Valor inicial Y:", min_value=y_min, max_value=y_max, value=y_min, format="%.3f", step=0.5)
with col2:
    y_end = st.number_input("Valor final Y:", min_value=y_min, max_value=y_max, value=y_max, format="%.3f", step=0.5)

lineas = st.slider("Número de líneas:", min_value=1, max_value=10, value=2)

if st.button("✔ Generar líneas"):
    st.warning("Aún no implementado", icon="😕")
    st.balloons()
    #cálculos
    #df = calcular_lineas(y_start, y_end, z_min, lineas)    
    #st.session_state.df_dist = calcular_distancias(st.session_state.df,center_z, líneas)
    #st.session_state.df_dist_motor = calcular_distancias_motor(st.session_state.df, center_z, ini_b, ini_a, ini_c)

