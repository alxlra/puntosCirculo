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
def calcular_distancias_motor(df, ini_a, ini_b, ini_c, offset=True):
    """Calcula las distancias de movimiento entre cada punto."""
    df_dist = pd.DataFrame(columns=["Carro A", "Carro B", "Carro C"])
    puntos = len(df)
    i=0
    if offset:
        df_dist.loc[len(df_dist)] = [df.loc[i]["X"] + df.loc[i]["Y"] + 2.5, df.loc[i]["X"] - df.loc[i]["Y"] - 2.5, df.loc[i]["X"]-df.loc[i]["Z"] - 2.5] 
    else:
        df_dist.loc[len(df_dist)] = [df.loc[i]["X"] + df.loc[i]["Y"], df.loc[i]["X"] - df.loc[i]["Y"] , df.loc[i]["X"]-df.loc[i]["Z"]] 
    
    for i in range(len(df)-1):
        dist_x = df.loc[(i + 1) % puntos]["X"] - df.loc[i]["X"]
        dist_y = df.loc[(i + 1) % puntos]["Y"] - df.loc[i]["Y"]
        dist_z = df.loc[(i + 1) % puntos]["Z"] - df.loc[i]["Z"]
        df_dist.loc[len(df_dist)] = [dist_x+dist_y, dist_x-dist_y, dist_x- dist_z]

    # Regreso al punto inicial
    i=0
    if offset:
        df_dist.loc[len(df_dist)] = [-(df.loc[i]["X"] + df.loc[i]["Y"] + 2.5), -(df.loc[i]["X"] - df.loc[i]["Y"] - 2.5), -(df.loc[i]["X"]-df.loc[i]["Z"] - 2.5)] 
    else:
        df_dist.loc[len(df_dist)] = [-(df.loc[i]["X"] + df.loc[i]["Y"]), -(df.loc[i]["X"] - df.loc[i]["Y"]), -(df.loc[i]["X"]-df.loc[i]["Z"])]

    # Cambio a código G
    df_dist["Carro A"] = df_dist["Carro A"]*0.2
    df_dist["Carro B"] = df_dist["Carro B"]*(-0.2)
    df_dist["Carro C"] = df_dist["Carro C"]*(-0.2)
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