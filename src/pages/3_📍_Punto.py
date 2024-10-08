# app.py
import streamlit as st
import math
import pandas as pd
from matplotlib import pyplot as plt

from preferencias import leer_preferencias
from calculos import *



def graficar_puntos(df):
    plt.style.use("ggplot")
    st.subheader("Gráfica de los puntos generados")
    # Crear una gráfica de dispersión
    plt.figure(figsize=(8, 8))
    plt.scatter(df["X"], df["Y"], color='red', marker='o')
    #plt.title("Gráfica de Dispersión")
    #plt.xlabel("X")
    #plt.ylabel("Y")
    plt.grid(True)

    # Mostrar la gráfica en Streamlit
    st.pyplot(plt)
#--------------------

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

if not preferencias:
    st.error("No hay preferencias guardadas.", icon="ℹ")

st.title("📍 Movimiento hacia un punto")

col1,col2 = st.columns(2)
with col1:
    center_x = st.number_input("Coordenada X:", min_value=x_min, max_value=x_max, value=21.83, format="%.3f", step=0.5)
    levantar = st.checkbox("Levantar pluma al dibujar", value=True, help="Levanta la pluma al inicio y al final del dibujo.")
    offset = st.checkbox("Quitar offset de carros", value=True, help="Quita el offset del inicio de los carros en el código G.")
with col2:
    center_y = st.number_input("Coordenada Y:", min_value=y_min, max_value=y_max, value=12.66, format="%.3f", step=0.5)


if st.button("✔ Generar"):
    #cálculos
    df = calcular_punto(center_x, center_y, center_z, levantar)    
    df_dist = calcular_distancias(df)
    df_dist_motor = calcular_distancias_motor(df, ini_b, ini_a, ini_c, offset)


    st.divider()

    st.write("Movimientos generados: ", str(len(df)))

    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Coordenadas generadas")
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
    
        