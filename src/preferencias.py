import json
# Función para leer las preferencias desde el archivo JSON
def leer_preferencias():
    try:
        with open('preferencias.json', 'r') as f:
            preferencias = json.load(f)
        return preferencias
    except FileNotFoundError:
        return None
    
def guardar_preferencias(json_data):
    with open('preferencias.json', 'w') as f:
        json.dump(json_data, f)