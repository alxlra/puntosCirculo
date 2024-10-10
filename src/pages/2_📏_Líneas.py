import streamlit as st
import math
import pandas as pd
from matplotlib import pyplot as plt

from preferencias import leer_preferencias
from calculos import *

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
escala = preferencias.get("escala", 0.2)

if not preferencias:
    st.error("No hay preferencias guardadas.", icon="ℹ")

st.title("📏 Generador de línea")

col1,col2 = st.columns(2)
with col1:
    x_start = st.number_input("Valor X inicial:", min_value=x_min, max_value=x_max, value=20.0, format="%.3f", step=0.5)
    x_end = st.number_input("Valor X final :", min_value=x_min, max_value=x_max, value=26.0, format="%.3f", step=0.5)
with col2:
    y_start = st.number_input("Valor Y inicial:", min_value=y_min, max_value=y_max, value=12.0, format="%.3f", step=0.5)
    y_end = st.number_input("Valor Y final :", min_value=y_min, max_value=y_max, value=12.0, format="%.3f", step=0.5)
levantar = st.checkbox("Levantar pluma al dibujar", value=True, help="Levanta la pluma al inicio y al final del dibujo.")
offset = st.checkbox("Quitar offset de carros", value=False, help="Quita el offset del inicio de los carros en el código G.")

if st.button("✔ Generar línea"):
    #cálculos
    df = calcular_linea(x_start, y_start, x_end, y_end, z_min, levantar)
    df_dist = calcular_distancias(df)
    df_dist_motor = calcular_distancias_motor(df, escala)

    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Puntos generados")
        st.dataframe(df)
        #st.button("Descargar puntos", df.to_csv("puntos.csv", index=False))
        csv = df.to_csv(index=False)  # Convertir el dataframe a CSV
        st.download_button(
            label="💾 Descargar puntos",
            data=csv,
            file_name="puntos.csv",
            mime="text/csv"
        )
    
    with col2:
        st.subheader("Carros código G")
        st.dataframe(df_dist_motor)
        #st.button("Descargar movimientos", df.to_csv("movimientos.csv", index=False))
        csv3 = df_dist_motor.to_csv(index=False)  # Convertir el dataframe a CSV
        st.download_button(
            label="💾 Descargar movimientos motor",
            data=csv3,
            file_name="movimientos_motor.csv",
            mime="text/csv"
        )
    st.divider()
    
    #gráfica de los puntos
    graficar_puntos(df)

