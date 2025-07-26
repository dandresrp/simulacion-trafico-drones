from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from modelo_ciudad import ModeloCiudad


# Visualización mejorada: obstáculos, zonas de exclusión y drones con batería baja
def dron_portrayal(agent):
    # Obstáculos y zonas de exclusión
    if hasattr(agent, 'tipo'):
        if agent.tipo == 'obstaculo':
            return {
                "Shape": "rect",
                "w": 1,
                "h": 1,
                "Filled": "true",
                "Color": "#888888",
                "Layer": 0
            }
        elif agent.tipo == 'hospital':
            return {
                "Shape": "rect",
                "w": 1,
                "h": 1,
                "Filled": "true",
                "Color": "#FF0000",
                "Layer": 0
            }
        elif agent.tipo == 'aeropuerto':
            return {
                "Shape": "rect",
                "w": 1,
                "h": 1,
                "Filled": "true",
                "Color": "#FFA500",
                "Layer": 0
            }
    # Drones
    if hasattr(agent, 'entregado') and agent.entregado:
        color = "#00FF00"  # Verde: entregado
    elif hasattr(agent, 'bateria') and agent.bateria < 20:
        color = "#FFFF00"  # Amarillo: batería baja
    else:
        color = "#0000FF"  # Azul: en ruta
    return {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.7,
        "Color": color,
        "Layer": 1
    }


grid = CanvasGrid(dron_portrayal, 20, 20, 500, 500)

# Gráfica de métricas en tiempo real
chart = ChartModule([
    {"Label": "Colisiones", "Color": "#FF0000"},
    {"Label": "Entregas", "Color": "#00FF00"},
    {"Label": "Desvios", "Color": "#FFA500"}
])

model_params = {
    "n_drones": UserSettableParameter('slider', 'Cantidad de drones', 10, 1, 100, 1),
    "algoritmo": UserSettableParameter('choice', 'Algoritmo', value='A*', choices=['A*', 'Dijkstra'])
}

server = ModularServer(
    ModeloCiudad,
    [grid, chart],
    "Simulación de Tráfico de Drones",
    model_params
)

if __name__ == "__main__":
    server.port = 8521
    server.launch()
