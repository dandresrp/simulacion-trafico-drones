from modelo_ciudad import ModeloCiudad
import json

if __name__ == "__main__":
    # Parámetros por defecto; ajusta si lo deseas
    modelo = ModeloCiudad(width=20, height=20, n_drones=10, algoritmo="A*")
    # Safety cap para evitar loops infinitos en caso de estados patológicos
    reporte = modelo.run_until_done(max_steps=5000)
    print(json.dumps(reporte, ensure_ascii=False, indent=2))
