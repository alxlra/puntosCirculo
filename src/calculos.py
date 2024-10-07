import math
import pandas as pd

# Función para generar puntos en el perímetro del círculo
def calcular_puntos(center_x, center_y, z, radio, puntos, levantar=False):
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
def calcular_distancias_motor(df, z, ini_a, ini_b, ini_c, puntos=4):
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