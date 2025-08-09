import networkx as nx
from mesa import Agent
import math
from typing import List, Tuple, Optional


class Dron(Agent):
    def __init__(self, unique_id, model, pos_ini: Tuple[int, int], pos_dest: Tuple[int, int], algoritmo: str):
        super().__init__(unique_id, model)
        self.pos_ini = pos_ini
        self.pos_dest = pos_dest
        self.algoritmo = algoritmo
        self.ruta: List[Tuple[int, int]] = []
        self.bateria = 100
        self.entregado = False
        self.paso_actual = 0
        self._bateria_reportada = False
        self.pasos_sin_mover = 0
        self.ruta = self.calcular_ruta()

    def calcular_ruta(self, desde: Optional[Tuple[int, int]] = None, hasta: Optional[Tuple[int, int]] = None) -> List[Tuple[int, int]]:
        G = self.model.G
        origen = desde if desde is not None else self.pos_ini
        destino = hasta if hasta is not None else self.pos_dest
        try:
            if self.algoritmo == 'A*':
                return nx.astar_path(G, origen, destino, heuristic=self.euclidiana)
            else:
                return nx.dijkstra_path(G, origen, destino)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return [origen]

    def euclidiana(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def step(self):
        if self.entregado:
            return
        if self.bateria <= 0:
            if not self._bateria_reportada and hasattr(self.model, "fallas_bateria"):
                self.model.fallas_bateria += 1
                self._bateria_reportada = True
            return

        pos_actual = self.pos if getattr(self, "pos", None) is not None else self.pos_ini
        if not self.ruta or self.ruta[0] != pos_actual:
            self.ruta = self.calcular_ruta(desde=pos_actual, hasta=self.pos_dest)
            self.paso_actual = 0

        next_idx = self.paso_actual + 1
        if next_idx >= len(self.ruta):
            if pos_actual == self.pos_dest:
                self.entregado = True
                if hasattr(self.model, "tiempos_entrega"):
                    self.model.tiempos_entrega.append(self.paso_actual)
                if hasattr(self.model, "entregas"):
                    self.model.entregas += 1
            return

        nueva_pos = self.ruta[next_idx]

        cellmates = self.model.grid.get_cell_list_contents([nueva_pos])
        if any(isinstance(a, Dron) and a.unique_id != self.unique_id for a in cellmates):
            if hasattr(self.model, "colisiones"):
                self.model.colisiones += 1
            if hasattr(self.model, "desvios"):
                self.model.desvios += 1
            self.ruta = self.calcular_ruta(desde=pos_actual, hasta=self.pos_dest)
            self.paso_actual = 0
            self.pasos_sin_mover += 1
            prev = self.bateria
            self.bateria = max(0, self.bateria - 1)
            if self.bateria <= 0 and prev > 0 and not self._bateria_reportada and hasattr(self.model, "fallas_bateria"):
                self.model.fallas_bateria += 1
                self._bateria_reportada = True
            return

        self.model.grid.move_agent(self, nueva_pos)
        self.paso_actual = next_idx
        self.pasos_sin_mover = 0

        prev = self.bateria
        self.bateria = max(0, self.bateria - 1)
        if self.bateria <= 0 and prev > 0 and not self._bateria_reportada and hasattr(self.model, "fallas_bateria"):
            self.model.fallas_bateria += 1
            self._bateria_reportada = True

        if nueva_pos == self.pos_dest:
            self.entregado = True
            if hasattr(self.model, "tiempos_entrega"):
                self.model.tiempos_entrega.append(self.paso_actual)
            if hasattr(self.model, "entregas"):
                self.model.entregas += 1