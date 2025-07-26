from agente_dron import Dron
import random
import networkx as nx
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from agente_dron import Dron

class ModeloCiudad(Model):
    def __init__(self, width=20, height=20, n_drones=10, algoritmo='A*'):
        super().__init__()
        self.width = width
        self.height = height
        self.n_drones = n_drones
        self.algoritmo = algoritmo
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.G = nx.grid_2d_graph(width, height)
        self.colisiones = 0
        self.desvios = 0
        self.entregas = 0
        self.tiempos_entrega = []
        self._agregar_obstaculos()
        self._agregar_zonas_exclusion()
        self._crear_drones()
        self.datacollector = DataCollector(
            model_reporters={
                "Colisiones": lambda m: m.colisiones,
                "Desvios": lambda m: m.desvios,
                "Entregas": lambda m: m.entregas,
                "TiemposEntrega": lambda m: m.tiempos_entrega
            }
        )

    def _agregar_obstaculos(self):
        """Agrega edificios como obstáculos en la ciudad."""
        edificios = [(x, 10) for x in range(5, 15)]
        self.G.remove_nodes_from(edificios)
        for pos in edificios:
            self.grid.place_agent(Obstaculo(pos, 'obstaculo'), pos)

    def _agregar_zonas_exclusion(self):
        """Agrega zonas de exclusión: hospital y aeropuerto."""
        hospital = [(x, y) for x in range(2, 5) for y in range(2, 5)]
        aeropuerto = [(x, y) for x in range(15, 18) for y in range(15, 18)]
        self.G.remove_nodes_from(hospital + aeropuerto)
        for pos in hospital:
            self.grid.place_agent(Obstaculo(pos, 'hospital'), pos)
        for pos in aeropuerto:
            self.grid.place_agent(Obstaculo(pos, 'aeropuerto'), pos)

    def _crear_drones(self):
        """Crea y coloca los drones en posiciones válidas aleatorias."""
        posiciones_validas = list(self.G.nodes())
        random.shuffle(posiciones_validas)
        for i in range(self.n_drones):
            if len(posiciones_validas) < 2:
                break
            start = posiciones_validas.pop()
            end = posiciones_validas.pop()
            dron = Dron(i, self, start, end, self.algoritmo)
            self.grid.place_agent(dron, start)
            self.schedule.add(dron)

    def step(self):
        """Avanza la simulación un paso y recolecta métricas."""
        self.schedule.step()
        self.datacollector.collect(self)

class Obstaculo:
    def __init__(self, pos, tipo):
        self.pos = pos
        self.tipo = tipo


