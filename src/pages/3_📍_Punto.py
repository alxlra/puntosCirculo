# app.py
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
escala = preferencias.get("escala", 0.2)
ini_x = preferencias.get("ini_x", 8.125)
ini_y = preferencias.get("ini_y", 8.125)
ini_z = preferencias.get("ini_z", 5.625)

if not preferencias:
    st.error("No hay preferencias guardadas.", icon="ℹ")

st.title("📍 Movimiento hacia un punto")

col1,col2 = st.columns(2)
with col1:
    center_x = st.number_input("Coordenada X:", min_value=x_min, max_value=x_max, value=21.83, format="%.3f", step=0.5)
with col2:
    center_y = st.number_input("Coordenada Y:", min_value=y_min, max_value=y_max, value=12.66, format="%.3f", step=0.5)
levantar = st.checkbox("Levantar pluma al dibujar", value=False, help="Levanta la pluma al inicio y al final del dibujo.")
strInicio = "Iniciar en (X:"+ str(ini_x)+", Y:"+str(ini_y)+", Z:"+str(ini_z)+")"
offset = st.checkbox(strInicio, value=True, help="Se suma el punto de origen")

if st.button("✔ Generar"):
    if offset:
        df = calcular_punto(center_x-ini_x, center_y-ini_y, center_z-ini_z, levantar)
    else:
        df = calcular_punto(center_x, center_y, center_z, levantar)
    #cálculos
    df_dist = calcular_distancias(df)
    df_dist_motor, df_dist_suma = calcular_distancias_motor(df, escala)
    st.session_state.p_df = df
    st.session_state.p_df_dist_motor = df_dist_motor
    st.session_state.p_df_dist_suma = df_dist_suma


if "p_df" in st.session_state and "p_df_dist_motor" in st.session_state:
    df = st.session_state.p_df
    df_dist_motor = st.session_state.p_df_dist_motor
    df_dist_suma = st.session_state.p_df_dist_suma
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
        st.subheader("Carros código G 👼")
        df_dist_motor2 = df_dist_motor[["Carro B", "Carro C", "Carro A"]]
        st.dataframe(df_dist_motor2)
        #st.button("Descargar movimientos", df.to_csv("movimientos.csv", index=False))
        with st.expander("Archivo código G"):
            base_file_name = "punto"
            file_name = st.text_input("Nombre del archivo:", base_file_name, help="Nombre sin extensión, la extensión será txt")
            speed = st.slider("Velocidad:", min_value=25, max_value=200, value=100, step=25, help="Velocidad de los carros en mm/min")
            gcode_file = write_gcode(df_dist_motor, "g_code_file_p", speed)
            
            if file_name == "":  # Si no se ingresó un nombre
                file_name = base_file_name

            #Si file_name no contiene .txt se lo agrega
            if ".txt" not in file_name:
                file_name += ".txt"
    
            # Botón para descargar el archivo G-code
            with open(gcode_file, "r") as file:
                gcode_content = file.read()
            st.download_button(
                label="💾 Descargar código G",
                data=gcode_content,
                file_name=file_name,
                mime="text/plain"
            )
    
    st.divider()
    
        