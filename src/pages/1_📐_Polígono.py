# app.py
import streamlit as st
import math
import pandas as pd
from matplotlib import pyplot as plt

from preferencias import leer_preferencias

# Función para generar puntos en el perímetro del círculo
def calcular_puntos(center_x, center_y, z, radio, puntos, levantar=True):
    """Calcula los puntos en un círculo basado en las coordenadas del centro, el radio y la cantidad de puntos."""
    angulo_lados = (2 * math.pi) / puntos
    df = pd.DataFrame(columns=["X", "Y", "Z"])

    z_up = z+1
    if levantar:
        i=0
        x = center_x + radio * math.cos(angulo_lados * i)
        y = center_y + radio * math.sin(angulo_lados * i)
        df.loc[len(df)] = [x, y, z_up]  # Movimiento inicial

    for i in range(puntos):
        x = center_x + radio * math.cos(angulo_lados * i)
        y = center_y + radio * math.sin(angulo_lados * i)
        df.loc[len(df)] = [x, y, z]

    if levantar:
        x = center_x + radio * math.cos(angulo_lados * i)
        y = center_y + radio * math.sin(angulo_lados * i)
        df.loc[len(df)] = [x, y, z_up]  # Movimiento inicial
    return df

# Función para calcular las distancias de movimiento entre los puntos
def calcular_distancias(df, z, puntos):
    """Calcula las distancias de movimiento entre cada punto."""
    df_dist = pd.DataFrame(columns=["Movimiento X", "Movimiento Y", "Movimiento Z"])
    df_dist.loc[len(df_dist)] = [df.loc[0]["X"], df.loc[0]["Y"], z]  # Movimiento inicial

    for i in range(len(df)):
        dist_x = df.loc[(i + 1) % puntos]["X"] - df.loc[i]["X"]
        dist_y = df.loc[(i + 1) % puntos]["Y"] - df.loc[i]["Y"]
        df_dist.loc[len(df_dist)] = [dist_x, dist_y, z]

    return df_dist

# Función para calcular las distancias de movimiento entre los puntos
def calcular_distancias_motor(df, z, ini_a, ini_b, ini_c):
    """Calcula las distancias de movimiento entre cada punto."""
    df_dist = pd.DataFrame(columns=["Movimiento X", "Movimiento Y", "Movimiento Z"])
    z_up = z+1
    i=0
    df_dist.loc[len(df_dist)] = [df.loc[i]["X"] + df.loc[i]["Y"] - ini_a, df.loc[i]["X"] - df.loc[i]["Y"] - ini_b, df.loc[i]["X"]-z - ini_c] 

    for i in range(len(df)):
        dist_x = df.loc[(i + 1) % puntos]["X"] - df.loc[i]["X"]
        dist_y = df.loc[(i + 1) % puntos]["Y"] - df.loc[i]["Y"]
        dist_z = df.loc[(i + 1) % puntos]["Z"] - df.loc[i]["Z"]
        df_dist.loc[len(df_dist)] = [dist_x+dist_y, dist_x-dist_y, dist_x- dist_z]

    # Regreso al punto inicial
    i=0
    df_dist.loc[len(df_dist)] = [-(df.loc[i]["X"] + df.loc[i]["Y"] - ini_a), -(df.loc[i]["X"] - df.loc[i]["Y"] - ini_b), -(df.loc[i]["X"]-z - ini_c)] 

    #código G
    df_dist["Movimiento X"] = df_dist["Movimiento X"]*0.2
    df_dist["Movimiento Y"] = df_dist["Movimiento Y"]*(-0.2)
    df_dist["Movimiento Z"] = df_dist["Movimiento Z"]*(-0.2)
    return df_dist

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

st.title("📐 Generador de puntos de un polígono")

col1,col2 = st.columns(2)
with col1:
    center_x = st.number_input("Coordenada X del centro:", min_value=x_min, max_value=x_max, value=21.83, format="%.3f", step=0.5)
    radio = st.number_input("Radio:", min_value=1.0, max_value=10.0, value=4.0, format="%.2f", step=0.5)
    levantar = st.checkbox("Levantar pluma al dibujar", value=True, help="Levanta la pluma al inicio y al final del dibujo.")
with col2:
    center_y = st.number_input("Coordenada Y del centro:", min_value=y_min, max_value=y_max, value=12.66, format="%.3f", step=0.5)
    puntos = st.slider("Número de puntos:", min_value=2, max_value=20, value=10)


#puntos = st.slider("Número de puntos:", min_value=3, max_value=30, value=15)

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["X", "Y", "Z"])

if "df_dist" not in st.session_state:
    st.session_state.df_dist = pd.DataFrame(columns=["Movimiento X", "Movimiento Y", "Movimiento Z"])

if "df_dist_motor" not in st.session_state:
    st.session_state.df_dist_motor = pd.DataFrame(columns=["Movimiento X", "Movimiento Y", "Movimiento Z"])

if st.button("✔ Generar puntos"):
    #cálculos
    st.session_state.df = calcular_puntos(center_x, center_y, center_z, radio, puntos, levantar)    
    st.session_state.df_dist = calcular_distancias(st.session_state.df,center_z, puntos)
    st.session_state.df_dist_motor = calcular_distancias_motor(st.session_state.df, center_z, ini_b, ini_a, ini_c)

# ------------
placeholder = st.empty() #contenedor dinámico

#si existe en sesión, imprime resultados
if not st.session_state.df.empty and not st.session_state.df_dist.empty:

    df = st.session_state.df
    df_dist = st.session_state.df_dist
    df_dist_motor = st.session_state.df_dist_motor
    with placeholder.container():
        st.divider()

        st.write("Puntos generados: ", str(len(df)))

        col1,col2,col3 = st.columns(3)
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
            st.subheader("Movimientos")
            st.dataframe(df_dist)
            #st.button("Descargar movimientos", df.to_csv("movimientos.csv", index=False))
            csv2 = df_dist.to_csv(index=False)  # Convertir el dataframe a CSV
            st.download_button(
                label="💾 Descargar movimientos",
                data=csv2,
                file_name="movimientos.csv",
                mime="text/csv"
            )
        with col3:
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

        if st.button("✖ Borrar tablas"): #borra de sesión
            del st.session_state["df"]
            del st.session_state["df_dist"]
            placeholder.empty()
        