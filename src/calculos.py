import streamlit as st
import math
import pandas as pd
from matplotlib import pyplot as plt

# Función para generar puntos en el perímetro del círculo
def calcular_puntos(center_x, center_y, z, radio, puntos, levantar=False, angulo_incial=0):
    """Calcula los puntos en un círculo basado en las coordenadas del centro, el radio y la cantidad de puntos."""
    angulo_lados = (2 * math.pi) / puntos                                                                                                                                                                        
    #angulo_incial = math.pi*(0.75+0.5)
    angulo_incial = math.radians(angulo_incial)
    df = pd.DataFrame(columns=["X", "Y", "Z"])
    z_up = z+1
    if levantar:
        x = center_x + radio * math.cos(angulo_incial+angulo_lados * 0)
        y = center_y + radio * math.sin(angulo_incial+angulo_lados * 0)
        df.loc[len(df)] = [x, y, z_up]  # Movimiento inicial

    for i in range(puntos):
        x = center_x + radio * math.cos(angulo_incial+angulo_lados * i)
        y = center_y + radio * math.sin(angulo_incial+angulo_lados * i)
        df.loc[len(df)] = [x, y, z]

    x = center_x + radio * math.cos(angulo_incial+angulo_lados * 0)
    y = center_y + radio * math.sin(angulo_incial+angulo_lados * 0)
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
def calcular_distancias_motor(df, escala=0.2, ini_a=0.0, ini_b=0, ini_c=0):
    """Calcula las distancias de movimiento entre cada punto."""
    # Crear un DataFrame para almacenar los movimientos
    df_dist = pd.DataFrame(columns=["Carro A", "Carro B", "Carro C"])
    df_last_dist = pd.DataFrame(columns=["Carro A", "Carro B", "Carro C"])
    last_dist = [0,0,0]

    # Calcular el movimiento inicial del origen al primer punto
    dist_x = df.loc[0]["X"] - 0  # Del origen al primer punto
    dist_y = df.loc[0]["Y"] - 0
    dist_z = df.loc[0]["Z"] - 0
    mov_A = (dist_x - dist_y) / escala
    mov_B = (dist_x + dist_y) / escala
    mov_C = (dist_x - dist_z) / escala
    df_dist.loc[len(df_dist)] = [mov_A, mov_B, mov_C]
    last_dist = [last_dist[0]+mov_A, last_dist[1]+mov_B, last_dist[2]+mov_C]
    df_last_dist.loc[len(df_last_dist)] = last_dist

    # Calcular los movimientos entre los puntos
    num_puntos = len(df)
    for i in range(num_puntos-1):
        next_index = (i + 1) % num_puntos  # Para cerrar el polígono al volver al primer punto
        dist_x = df.loc[next_index]["X"] - df.loc[i]["X"]
        dist_y = df.loc[next_index]["Y"] - df.loc[i]["Y"]
        dist_z = df.loc[next_index]["Z"] - df.loc[i]["Z"]
        
        mov_A = (dist_x - dist_y) / escala
        mov_B = (dist_x + dist_y) / escala
        mov_C = (dist_x - dist_z) / escala
        df_dist.loc[len(df_dist)] = [mov_A, mov_B, mov_C]
        last_dist = [last_dist[0]+mov_A, last_dist[1]+mov_B, last_dist[2]+mov_C]
        df_last_dist.loc[len(df_last_dist)] = last_dist

    #dist_x = df.loc[0]["X"]-df.loc[len(df)-1]["X"]  # Del primer punto al origen
    #dist_y = -df.loc[0]["Y"] -df.loc[len(df)-1]["Y"]
    #dist_z = df.loc[0]["Z"] -df.loc[len(df)-1]["Z"]
    #mov_A = (dist_x + dist_y) / escala
    #mov_B = (dist_x - dist_y) / escala
    #mov_C = (dist_x - dist_z) / escala
    #df_dist.loc[len(df_dist)] = [mov_A, mov_B, mov_C]
    last_dist = [-last_dist[0], -last_dist[1], -last_dist[2]]
    
    df_last_dist.loc[len(df_last_dist)] = [0,0,0]
    df_dist.loc[len(df_dist)] = [last_dist[0], last_dist[1], last_dist[2]]
    
    #sumar offsets
    df_last_dist["Carro A"] = df_last_dist["Carro A"] + ini_a
    df_last_dist["Carro B"] = df_last_dist["Carro B"] + ini_b
    df_last_dist["Carro C"] = df_last_dist["Carro C"] + ini_c
    df_last_dist = df_last_dist[["Carro B", "Carro C", "Carro A"]]

    df_dist["Carro A"] = -df_dist["Carro A"]
    df_dist["Carro C"] = -df_dist["Carro C"]


    return df_dist, df_last_dist


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

def convertir_unidad(original, unidad, escala=1.0):
    if unidad == 0: #Centímetros a angelitos
        nueva = original / escala
    else:
        nueva = original * escala
    return float(nueva)

def write_gcode(df, file_name, speed):
    file_name="src/files/"+file_name
    with open(file_name, "w") as file:
        for y, x, z in zip(df["Carro A"], df["Carro B"], df["Carro C"]):
            file.write(f"G1 Y{y} X{x} Z{z} F{speed}\n")
    return file_name