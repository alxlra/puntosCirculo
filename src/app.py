# app.py
import streamlit as st
import math
import pandas as pd

def puntoX(center_x, center_y, y,radio, pos=True):
    if pos:
        return math.sqrt(radio**2 - (y-center_y)**2) + center_x
    return -math.sqrt(radio**2 - (y-center_y)**2) + center_x

st.title("Generador de puntos de un círculo")
center_x = st.number_input("Escribe la coordenada X del centro:", min_value=2, max_value=20, value=6)
center_y = st.number_input("Escribe la coordenada Y del centro:", min_value=2, max_value=20, value=6)
radio = st.number_input("Escribe el radio:", min_value=1, max_value=20, value=4)

puntos = st.slider("Número de puntos:", min_value=4, max_value=30, value=15)

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["X", "Y"])

if "df_dist" not in st.session_state:
    st.session_state.df_dist = pd.DataFrame(columns=["Movimiento X", "Movimiento Y"])

if st.button("Generar puntos"):


    y = 0
    x = 0
    angulo_lados = (2*math.pi)/puntos
    df = pd.DataFrame(columns=["X", "Y"])
    dist_x = 0
    dist_y = 0
    for i in range(puntos):
        x = center_x + radio*math.cos(angulo_lados*i)
        y = center_y + radio*math.sin(angulo_lados*i)
        df.loc[len(df)] = [x, y]
        #st.write(f"({x}, {y})")
    st.session_state.df = df

    df_dist = pd.DataFrame(columns=["Movimiento X", "Movimiento Y"])
    for i in range(len(df)):
        dist_x = abs(df.loc[i]["X"] - df.loc[(i+1)%puntos]["X"])
        dist_y = abs(df.loc[i]["Y"] - df.loc[(i+1)%puntos]["Y"])
        #st.write(f"({dist_x}, {dist_y})")
        df_dist.loc[len(df_dist)] = [dist_x, dist_y]
    st.session_state.df_dist = df_dist

placeholder = st.empty() #contenedor dinámico

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
                label="Descargar puntos",
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
                label="Descargar puntos",
                data=csv2,
                file_name="movimientos.csv",
                mime="text/csv"
            )

        if st.button("Borrar tablas"):
            del st.session_state["df"]
            del st.session_state["df_dist"]
            placeholder.empty()
        