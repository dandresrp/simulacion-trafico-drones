from modelo_ciudad import ModeloCiudad
import json

if __name__ == "__main__":
    modelo = ModeloCiudad(width=20, height=20, n_drones=10, algoritmo="A*")
    reporte = modelo.run_until_done(max_steps=5000)
    print(json.dumps(reporte, ensure_ascii=False, indent=2))
