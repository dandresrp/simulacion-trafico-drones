import networkx as nx
from mesa import Agent
import math

class Dron(Agent):
    def __init__(self, unique_id, model, pos_ini, pos_dest, algoritmo):
        super().__init__(unique_id, model)
        self.pos_ini = pos_ini
        self.pos_dest = pos_dest
        self.algoritmo = algoritmo
        self.ruta = self.calcular_ruta()
        self.bateria = 100
        self.entregado = False
        self.paso_actual = 0

    def calcular_ruta(self):
        G = self.model.G
        try:
            if self.algoritmo == 'A*':
                return nx.astar_path(G, self.pos_ini, self.pos_dest, heuristic=self.euclidiana)
            else:
                return nx.dijkstra_path(G, self.pos_ini, self.pos_dest)
        except nx.NetworkXNoPath:
            return [self.pos_ini]

    def euclidiana(self, a, b):
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

    def step(self):
        if self.entregado or self.paso_actual >= len(self.ruta):
            return
        nueva_pos = self.ruta[self.paso_actual]
        # Detección simple de colisión
        cellmates = self.model.grid.get_cell_list_contents([nueva_pos])
        if any(isinstance(a, Dron) and a.unique_id != self.unique_id for a in cellmates):
            self.model.colisiones += 1
            self.model.desvios += 1
            # Desviación: recalcula ruta
            self.ruta = self.calcular_ruta()
            self.paso_actual = 0
            return
        self.model.grid.move_agent(self, nueva_pos)
        self.paso_actual += 1
        self.bateria -= 1
        if nueva_pos == self.pos_dest:
            self.entregado = True
            self.model.tiempos_entrega.append(self.paso_actual)
            self.model.entregas += 1
