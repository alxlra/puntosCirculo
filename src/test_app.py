#Para probar: pytest /code/src/test_app.py

import pytest
import pandas as pd
from app import calcular_puntos, calcular_distancias

def test_calcular_puntos():
    # Prueba para calcular puntos en un círculo con centro (0, 0), radio 1 y 4 puntos
    center_x, center_y, radio, puntos = 6, 6, 1, 4
    df = calcular_puntos(center_x, center_y, radio, puntos)

    # Verifica que el DataFrame tiene 4 puntos
    assert len(df) == puntos

    # Verifica que las coordenadas sean las esperadas
    expected_points = [(7, 6), (6, 7), (5, 6), (6, 5)]  # Valores esperados
    for i, (x, y) in enumerate(expected_points):
        assert round(df.loc[i, "X"], 5) == x
        assert round(df.loc[i, "Y"], 5) == y

def test_calcular_distancias():
    # Crea un DataFrame de puntos para la prueba
    #data = {"X": [7, 6, 5, 6], "Y": [6, 7, 6, 5]}
    data = {"X": [7, 6, 5, 6], "Y": [6, 7, 6, -5]}
    df = pd.DataFrame(data)
    puntos = 4

    # Calcula las distancias
    df_dist = calcular_distancias(df, puntos)

    # Verifica que el DataFrame tiene 5 filas
    assert len(df_dist) == puntos + 1 

    # Verifica las distancias de movimiento
    expected_distances = [(7, 6), (-1, 1), (-1, -1), (1, -1),(1, 1)]  # Valores esperados
    for i, (dx, dy) in enumerate(expected_distances):
        assert df_dist.loc[i, "Movimiento X"] == dx
        assert df_dist.loc[i, "Movimiento Y"] == dy
