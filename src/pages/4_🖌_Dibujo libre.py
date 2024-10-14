# app.py
import streamlit as st
import math
import pandas as pd
import numpy as np
from streamlit_drawable_canvas import st_canvas
import cv2

from preferencias import leer_preferencias
from calculos import *

drawing_mode = "line"
stroke_width = 14
stroke_color = "#000000"
bg_color = "#FFFFFF"


#--------------------

# Leer y mostrar las preferencias guardadas
preferencias = leer_preferencias()
if not preferencias:
    st.error("No hay preferencias guardadas.", icon="ℹ")
ini_a = preferencias.get("ini_a", 0.0)
ini_b = preferencias.get("ini_b", 16.25)
ini_c = preferencias.get("ini_c", 2.5)
z_min = preferencias.get("z_min", 5.625)
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

st.title("🖌 Dibujo libre")
st.write("Dibuja una línea en el lienzo y presiona el botón para generar los puntos principales.")

drawing_mode = st.selectbox("Modo de dibujo", ["freedraw", "line"])

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=None,
    update_streamlit=True,
    height=240,
    width=240,
    drawing_mode=drawing_mode,
    point_display_radius=0,
    key="canvas",
)
levantar = st.checkbox("Levantar pluma al dibujar", value=True, help="Levanta la pluma al inicio y al final del dibujo.")
#strInicio = "Iniciar en (X:"+ str(ini_x)+", Y:"+str(ini_y)+", Z:"+str(ini_z)+")"
#offset = st.checkbox(strInicio, value=False, help="Se suma el punto de origen")

if st.button("✔ Generar puntos"):    
    # 1. Cargar imagen en escala de grises
    img = canvas_result.image_data
    img = np.array(img, dtype=np.uint8).copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Binarizar la imagen (convertirla a blanco y negro)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # 3. Invertir la imagen para que la línea sea blanca y el fondo negro
    binary = cv2.bitwise_not(binary)

    # 4. Encontrar el esqueleto de la línea
    skeleton = np.zeros(binary.shape, np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    done = False
    while not done:
        eroded = cv2.erode(binary, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(binary, temp)
        skeleton = cv2.bitwise_or(skeleton, temp)
        binary = eroded.copy()

        if cv2.countNonZero(binary) == 0:
            done = True

    # 5. Encontrar los puntos principales de la línea usando detección de esquinas
    corners = cv2.goodFeaturesToTrack(skeleton, maxCorners=25, qualityLevel=0.25, minDistance=10)
    if corners is not None and len(corners) > 0:
        corners = corners.astype(int)

        # 6. Dibujar los puntos principales en la imagen original
        for i in corners:
            x, y = i.ravel()
            cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

        # 7. Crear un DataFrame con las coordenadas de los puntos principales
        vertices = [(int(x), int(y)) for [[x, y]] in corners]
        df = pd.DataFrame(vertices, columns=["X", "Y"])
        df["Z"] = z_min
        df["X"] = df["X"] * y_max / 240
        df["Y"] = df["Y"] * y_max / 240

        # 8. Mostrar la imagen con los puntos detectados en Streamlit
        st.image(img, channels="BGR", caption="Puntos principales detectados")


        #cálculos
        #df = calcular_punto(center_x, center_y, center_z, levantar)    
        #df_dist = calcular_distancias(df)
        df_dist_motor, df_dist_suma = calcular_distancias_motor(df, escala)

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
            st.dataframe(df_dist_motor)
            #st.button("Descargar movimientos", df.to_csv("movimientos.csv", index=False))
            csv3 = df_dist_motor.to_csv(index=False)  # Convertir el dataframe a CSV
            st.download_button(
                label="💾 Descargar movimientos motor",
                data=csv3,
                file_name="movimientos_motor.csv",
                mime="text/csv"
            )
    else:
        st.warning("No se encontraron puntos principales en la imagen.")
    
        