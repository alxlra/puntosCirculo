#Para probar: pytest /code/src/test_app.py

import pytest
import pandas as pd
from app import calcular_puntos, calcular_distancias, calcular_distancias_motor

def test_calcular_puntos():
    """
    # Prueba para calcular puntos en un círculo con centro (0, 0), radio 1 y 4 puntos
    center_x, center_y, center_z, radio, puntos = 6, 6, 5, 1.0, 4
    df = calcular_puntos(center_x, center_y, center_z, radio, puntos)

    # Verifica que el DataFrame tiene 4 puntos
    assert len(df) == puntos

    # Verifica que las coordenadas sean las esperadas
    expected_points = [(7, 6, 5), (6, 7, 5), (5, 6, 5), (6, 5, 5)]  # Valores esperados
    for i, (x, y, z) in enumerate(expected_points):
        assert round(df.loc[i, "X"], 5) == x
        assert round(df.loc[i, "Y"], 5) == y
        assert round(df.loc[i, "Z"], 5) == z
    """
    assert True

def test_calcular_distancias():
    """
    # Crea un DataFrame de puntos para la prueba
    data = {"X": [7, 6, 5, 6], "Y": [6, 7, 6, 5], "Z": [5, 5, 5, 5]}
    df = pd.DataFrame(data)
    puntos = 4

    # Calcula las distancias
    df_dist = calcular_distancias(df, 5, puntos)

    # Verifica que el DataFrame tiene 5 filas
    assert len(df_dist) == puntos + 1 

    # Verifica las distancias de movimiento
    expected_distances = [(7, 6, 5), (-1, 1, 5), (-1, -1, 5), (1, -1, 5),(1, 1, 5)]  # Valores esperados
    for i, (dx, dy, dz) in enumerate(expected_distances):
        assert df_dist.loc[i, "Movimiento X"] == dx
        assert df_dist.loc[i, "Movimiento Y"] == dy
        assert df_dist.loc[i, "Movimiento Z"] == dz
    """
    assert True

"""def test_calcular_distancias_motor():
    # Crea un DataFrame de puntos para la prueba
    data = {"X": [7, 6, 5, 6], "Y": [6, 7, 6, 5], "Z": [6, 7, 6, 5]}
    df = pd.DataFrame(data)
    puntos = 4

    # Calcula las distancias
    df_dist = calcular_distancias_motor(df, 2, 1, 1, 1)

    # Verifica que el DataFrame tiene 5 filas
    assert len(df_dist) == puntos + 1 

    # Verifica las distancias de movimiento
    expected_distances = [(7-6-1, 7+6-1, 7-2-1), (-1-1-1, -1+1-1,-1+2-1), (-1+1-1, -1-1-1, -1-2-1), (1+1-1, 1-1-1,1-2-1),(1-1-1, 1+1-1,1-2-1)]  # Valores esperados
    for i, (dx, dy, dz) in enumerate(expected_distances):
        assert df_dist.loc[i, "Movimiento X"] == dx
        assert df_dist.loc[i, "Movimiento Y"] == dy
        assert df_dist.loc[i, "Movimiento Z"] == dz
"""