import streamlit as st
import math
from calculos import convertir_unidad
from preferencias import leer_preferencias

preferencias = leer_preferencias()
escala = preferencias.get("escala", 1.0)

st.title("👼 Conversor de unidades")
st.write("Convierte entre centímetros y angelitos. El dibujo y las coordenadas se realizan en centímetros, pero los motores se mueven en angelitos.")
st.markdown("La escala se modifica en [Configuración](./Configuración)")
st.write(1," movimiento de carro = ", escala," unidades de dibujo")

opciones = ["Centímetros a Angelitos", "Angelitos a Centímetros"]

if "unidad_nueva" not in st.session_state:
    st.session_state["unidad_nueva"] = 0.0

col1,col2, col3 = st.columns(3)
with col1:
    original = st.number_input("Unidad original:", value=0.0, format="%.3f", step=0.5)
with col2:
    unidad = st.selectbox("Unidades", opciones)
with col3:
    st.write("Unidad convertida")

if st.button("✔ Convertir"):
    indice_unidad = opciones.index(unidad)
    nueva = convertir_unidad(original, indice_unidad,escala)
    with col3:
        st.write(f"{nueva:.3f}")

    