# app.py
import streamlit as st
import math
import pandas as pd
from matplotlib import pyplot as plt

from preferencias import leer_preferencias
from calculos import *



#--------------------

# Leer y mostrar las preferencias guardadas
preferencias = leer_preferencias()
if not preferencias:
    st.error("No hay preferencias guardadas.", icon="ℹ")
ini_a = preferencias.get("ini_a", 0.0)
ini_b = preferencias.get("ini_b", 16.25)
ini_c = preferencias.get("ini_c", 2.5)
pos_z = preferencias.get("z_min", 5.625)
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

st.title("📐 Figura manual con puntos")
st.subheader("Datos del polígono")
col1,col2, col3 = st.columns(3)
with col1:
    pos_x = st.number_input("Coordenada X:", min_value=x_min, max_value=x_max, value=20.313, format="%.3f", step=0.5)
with col2:
    pos_y = st.number_input("Coordenada Y:", min_value=y_min, max_value=y_max, value=12.188, format="%.3f", step=0.5)
with col3:
    pos_z = st.number_input("Coordenada Z:", min_value=y_min, max_value=y_max, value=12.188, format="%.3f", step=0.5)


# Guardar los datos en la sesión
if "df_man" not in st.session_state:
    st.session_state.df_man = pd.DataFrame(columns=["X", "Y", "Z"])

if "df_dist_motor_man" not in st.session_state:
    st.session_state.df_dist_motor_man = pd.DataFrame(columns=["Carro A", "Carro B", "Carro C"])

if "df_dist_suma_man" not in st.session_state:
    st.session_state.df_dist_suma_man = pd.DataFrame(columns=["Carro A", "Carro B", "Carro C"])


col1,col2, col3 = st.columns(3)
with col1:
    if st.button("➕ Agregar punto"):
        df = st.session_state.df_man
        df.loc[len(df)] = [pos_x, pos_y, pos_z]
        
        st.session_state.df_man = df
with col2:
    if st.button("➖ Quitar último"):
        #quita último punto de df
        df = st.session_state.df_man
        df = df[:-1]
        st.session_state.df_man = df

st.dataframe(st.session_state.df_man)

if len(st.session_state.df_man) >= 1:
    levantar = st.checkbox("Levantar pluma al dibujar", value=False, help="Levanta la pluma al inicio y al final del dibujo.")
    strInicio = "Iniciar en (X:"+ str(ini_x)+", Y:"+str(ini_y)+", Z:"+str(ini_z)+")"
    offset = st.checkbox(strInicio, value=True, help="Se suma el punto de origen")

    if st.button("✔ Generar puntos"):
        #cálculos
        df = st.session_state.df_man
        df_dist_motor_man, df_dist_suma_man = calcular_distancias_motor(df, escala)
        st.session_state.df_dist_motor_man = df_dist_motor_man
        st.session_state.df_dist_suma_man = df_dist_suma_man

if "df_man" in st.session_state and "df_dist_motor_man" in st.session_state and len(st.session_state.df_dist_motor_man)>0:
    df = st.session_state.df_man
    df_dist_motor = st.session_state.df_dist_motor_man
    df_dist_suma = st.session_state.df_dist_suma_man
    st.divider()

    st.write("Puntos generados: ", str(len(df)))

    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Carros código G 👼")
        df_dist_motor2 = df_dist_motor[["Carro B", "Carro C", "Carro A"]]
        st.dataframe(df_dist_motor2)
        #st.button("Descargar movimientos", df.to_csv("movimientos.csv", index=False))
        with st.expander("Archivo código G"):
            base_file_name = "figura_"+str(len(st.session_state.df_man))
            file_name = st.text_input("Nombre del archivo:", base_file_name, help="Nombre sin extensión, la extensión será txt")
            speed = st.slider("Velocidad:", min_value=25, max_value=200, value=100, step=25, help="Velocidad de los carros en mm/min")
            gcode_file = write_gcode(df_dist_motor, "g_code_file_fig", speed)

            if gcode_file is not None:
            
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
    #with col3:
    #    st.subheader("Carros posiciones 👼")
    #    st.dataframe(df_dist_suma)
    st.divider()
    
    #gráfica de los puntos
    graficar_puntos(df)



