import streamlit as st
import math
import pandas as pd
from matplotlib import pyplot as plt

# Función para generar puntos en el perímetro del círculo
def calcular_puntos(center_x, center_y, z, radio, puntos, levantar=False):
    """Calcula los puntos en un círculo basado en las coordenadas del centro, el radio y la cantidad de puntos."""
    angulo_lados = (2 * math.pi) / puntos
    df = pd.DataFrame(columns=["X", "Y", "Z"])
    z_up = z+1
    if levantar:
        x = center_x + radio * math.cos(angulo_lados * 0)
        y = center_y + radio * math.sin(angulo_lados * 0)
        df.loc[len(df)] = [x, y, z_up]  # Movimiento inicial

    for i in range(puntos):
        x = center_x + radio * math.cos(angulo_lados * i)
        y = center_y + radio * math.sin(angulo_lados * i)
        df.loc[len(df)] = [x, y, z]

    x = center_x + radio * math.cos(angulo_lados * 0)
    y = center_y + radio * math.sin(angulo_lados * 0)
    df.loc[len(df)] = [x, y, z]  # Movimiento inicial
    if levantar:
        df.loc[len(df)] = [x, y, z_up]  # Movimiento inicial

    #df["X"] = -df["X"]
    return df

# Función para generar puntos en el perímetro del círculo
def calcular_linea(x_start, y_start, x_end, y_end, z, levantar=False):
    """Calcula los puntos de una línea."""
    df = pd.DataFrame(columns=["X", "Y", "Z"])

    z_up = z+1
    if levantar:
        df.loc[len(df)] = [x_start, y_start, z_up]  # Movimiento inicial

    df.loc[len(df)] = [x_start, y_start, z]
    df.loc[len(df)] = [x_end, y_end, z] 

    if levantar:
        df.loc[len(df)] = [x_end, y_end, z_up]  # Movimiento inicial
    return df


# Función para generar un solo punto
def calcular_punto(x, y, z, levantar=False):
    """Calcula la posición de un punto."""
    df = pd.DataFrame(columns=["X", "Y", "Z"])

    z_up = z+1
    if levantar:
        i=0
        df.loc[len(df)] = [x, y, z_up]  # Movimiento inicial

    df.loc[len(df)] = [x, y, z]

    if levantar:
        df.loc[len(df)] = [x, y, z_up]  # Movimiento inicial
    return df


# Función para calcular las distancias de movimiento entre los puntos
def calcular_distancias(df):
    """Calcula las distancias de movimiento entre cada punto."""
    df_dist = pd.DataFrame(columns=["Movimiento X", "Movimiento Y", "Movimiento Z"])
    df_dist.loc[0] = [df.loc[0]["X"], df.loc[0]["Y"], df.loc[0]["Z"]]  # Movimiento inicial
    puntos = len(df)

    for i in range(len(df)-1):
        dist_x = df.loc[(i + 1) % puntos]["X"] - df.loc[i]["X"]
        dist_y = df.loc[(i + 1) % puntos]["Y"] - df.loc[i]["Y"]
        dist_z = df.loc[(i + 1) % puntos]["Z"] - df.loc[i]["Z"]
        df_dist.loc[len(df_dist)] = [dist_x, dist_y, dist_z]

    return df_dist

# Función para calcular las distancias de movimiento entre los puntos
def calcular_distancias_motor(df, escala=0.2):
    """Calcula las distancias de movimiento entre cada punto."""
    # Crear un DataFrame para almacenar los movimientos
    df_dist = pd.DataFrame(columns=["Carro A", "Carro B", "Carro C"])

    # Calcular el movimiento inicial del origen al primer punto
    dist_x = df.loc[0]["X"] - 0  # Del origen al primer punto
    dist_y = df.loc[0]["Y"] - 0
    dist_z = df.loc[0]["Z"] - 0
    mov_A = (dist_x + dist_y) * escala
    mov_B = (dist_x - dist_y) * -escala
    mov_C = (dist_x - dist_z) * -escala
    df_dist.loc[len(df_dist)] = [mov_A, mov_B, mov_C]

    # Calcular los movimientos entre los puntos
    num_puntos = len(df)
    for i in range(num_puntos-1):
        next_index = (i + 1) % num_puntos  # Para cerrar el polígono al volver al primer punto
        dist_x = df.loc[next_index]["X"] - df.loc[i]["X"]
        dist_y = df.loc[next_index]["Y"] - df.loc[i]["Y"]
        dist_z = df.loc[next_index]["Z"] - df.loc[i]["Z"]
        
        mov_A = (dist_x + dist_y) * escala
        mov_B = (dist_x - dist_y) * -escala
        mov_C = (dist_x - dist_z) * -escala
        df_dist.loc[len(df_dist)] = [mov_A, mov_B, mov_C]

    dist_x = 0-df.loc[0]["X"]  # Del primer punto al origen
    dist_y = 0-df.loc[0]["Y"] 
    dist_z = 0-df.loc[0]["Z"] 
    mov_A = (dist_x + dist_y) * escala
    mov_B = (dist_x - dist_y) * -escala
    mov_C = (dist_x - dist_z) * -escala
    df_dist.loc[len(df_dist)] = [mov_A, mov_B, mov_C]


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