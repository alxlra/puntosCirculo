# app.py
import streamlit as st
import math
import pandas as pd
from matplotlib import pyplot as plt

# Función para generar puntos en el perímetro del círculo
def calcular_puntos(center_x, center_y, radio, puntos):
    """Calcula los puntos en un círculo basado en las coordenadas del centro, el radio y la cantidad de puntos."""
    angulo_lados = (2 * math.pi) / puntos
    df = pd.DataFrame(columns=["X", "Y"])

    for i in range(puntos):
        x = center_x + radio * math.cos(angulo_lados * i)
        y = center_y + radio * math.sin(angulo_lados * i)
        df.loc[len(df)] = [x, y]

    return df

# Función para calcular las distancias de movimiento entre los puntos
def calcular_distancias(df, puntos):
    """Calcula las distancias de movimiento entre cada punto."""
    df_dist = pd.DataFrame(columns=["Movimiento X", "Movimiento Y"])
    df_dist.loc[len(df_dist)] = [df.loc[0]["X"], df.loc[0]["Y"]]  # Movimiento inicial

    for i in range(len(df)):
        dist_x = df.loc[(i + 1) % puntos]["X"] - df.loc[i]["X"]
        dist_y = df.loc[(i + 1) % puntos]["Y"] - df.loc[i]["Y"]
        df_dist.loc[len(df_dist)] = [dist_x, dist_y]

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



st.title("📐 Generador de puntos de un polígono")
center_x = st.slider("Coordenada X del centro:", min_value=2, max_value=20, value=6)
center_y = st.slider("Coordenada Y del centro:", min_value=2, max_value=20, value=6)
radio = st.slider("Radio:", min_value=1, max_value=10, value=4)

puntos = st.slider("Número de puntos:", min_value=4, max_value=30, value=15)

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["X", "Y"])

if "df_dist" not in st.session_state:
    st.session_state.df_dist = pd.DataFrame(columns=["Movimiento X", "Movimiento Y"])

if st.button("✔ Generar puntos"):
    #cálculos
    st.session_state.df = calcular_puntos(center_x, center_y, radio, puntos)    
    st.session_state.df_dist = calcular_distancias(st.session_state.df, puntos)

# ------------
placeholder = st.empty() #contenedor dinámico

#si existe en sesión, imprime resultados
if not st.session_state.df.empty and not st.session_state.df_dist.empty:

    df = st.session_state.df
    df_dist = st.session_state.df_dist
    with placeholder.container():
        st.divider()

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
        st.divider()
        
        #gráfica de los puntos
        graficar_puntos(df)

        if st.button("✖ Borrar tablas"): #borra de sesión
            del st.session_state["df"]
            del st.session_state["df_dist"]
            placeholder.empty()
        