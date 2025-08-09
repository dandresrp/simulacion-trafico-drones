from agente_dron import Dron
import random
import networkx as nx
from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from agente_dron import Dron
from statistics import mean
from typing import Dict, Any

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
        self.fallas_bateria = 0
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
        edificios = [(x, 10) for x in range(5, 15)]
        self.G.remove_nodes_from(edificios)
        for pos in edificios:
            obs = Obstaculo(f"obstaculo-{pos[0]}-{pos[1]}", self, pos, 'obstaculo')
            self.grid.place_agent(obs, pos)

    def _agregar_zonas_exclusion(self):
        hospital = [(x, y) for x in range(2, 5) for y in range(2, 5)]
        aeropuerto = [(x, y) for x in range(15, 18) for y in range(15, 18)]
        self.G.remove_nodes_from(hospital + aeropuerto)
        for pos in hospital:
            obs = Obstaculo(f"hospital-{pos[0]}-{pos[1]}", self, pos, 'hospital')
            self.grid.place_agent(obs, pos)
        for pos in aeropuerto:
            obs = Obstaculo(f"aeropuerto-{pos[0]}-{pos[1]}", self, pos, 'aeropuerto')
            self.grid.place_agent(obs, pos)

    def _crear_drones(self):
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
        self.schedule.step()
        self.datacollector.collect(self)

    # --- Terminación y reporte ---
    def _esta_bloqueado(self, dron: Dron) -> bool:
        """Un dron está bloqueado si:
        - no tiene ruta útil (ruta de longitud <= 1 desde su posición), o
        - ha estado varios pasos sin poder moverse (atasco/congestión),
        y aún no llegó al destino y no está sin batería.
        """
        try:
            pos_actual = dron.pos if getattr(dron, "pos", None) is not None else dron.pos_ini
            umbral_estancado = 10
            return (
                dron.bateria > 0
                and not dron.entregado
                and isinstance(getattr(dron, "ruta", []), list)
                and (len(dron.ruta) <= 1 or getattr(dron, "pasos_sin_mover", 0) >= umbral_estancado)
                and pos_actual != dron.pos_dest
            )
        except Exception:
            return False

    def terminada(self) -> bool:
        """La simulación termina cuando todos los drones están detenidos:
        entregados, sin batería o bloqueados sin ruta.
        """
        if not self.schedule.agents:
            return True
        for a in self.schedule.agents:
            if isinstance(a, Dron):
                if not (a.entregado or a.bateria <= 0 or self._esta_bloqueado(a)):
                    return False
        return True

    def generar_reporte(self, pasos_totales: int) -> Dict[str, Any]:
        total = self.n_drones
        entregas = self.entregas
        tasa_entrega = (entregas / total) if total > 0 else 0.0
        tiempos = list(self.tiempos_entrega)
        tiempo_prom = mean(tiempos) if tiempos else None
        tiempo_min = min(tiempos) if tiempos else None
        tiempo_max = max(tiempos) if tiempos else None
        bloqueados = 0
        for a in self.schedule.agents:
            if isinstance(a, Dron) and self._esta_bloqueado(a):
                bloqueados += 1

        recomendaciones = []
        if self.colisiones > 0:
            recomendaciones.append(
                "Reducir colisiones: introducir coordinación (prioridades/reservas), penalizar celdas congestionadas o añadir espera aleatoria."
            )
        if self.desvios > total:
            recomendaciones.append(
                "Muchos desvíos: revisar congestión y/o usar heurísticas con costo dinámico por ocupación."
            )
        if self.fallas_bateria > 0 or (tiempo_prom is not None and tiempo_prom > (self.width + self.height) / 2):
            recomendaciones.append(
                "Energía: acortar rutas, añadir estaciones de carga o planificar con presupuesto de batería."
            )
        if bloqueados > 0:
            recomendaciones.append(
                "Hay drones bloqueados sin ruta: reconsiderar obstáculos/zona de exclusión o permitir vías alternativas."
            )
        if self.algoritmo == 'Dijkstra':
            recomendaciones.append(
                "Probar A*: suele dar rutas más directas en rejillas con distancia euclídea."
            )

        return {
            "parametros": {
                "width": self.width,
                "height": self.height,
                "n_drones": self.n_drones,
                "algoritmo": self.algoritmo,
            },
            "resultados": {
                "pasos_totales": pasos_totales,
                "entregas": entregas,
                "tasa_entrega": tasa_entrega,
                "colisiones": self.colisiones,
                "desvios": self.desvios,
                "fallas_bateria": self.fallas_bateria,
                "drones_bloqueados": bloqueados,
                "tiempo_promedio_entrega": tiempo_prom,
                "tiempo_min_entrega": tiempo_min,
                "tiempo_max_entrega": tiempo_max,
            },
            "recomendaciones": recomendaciones,
        }

    def run_until_done(self, max_steps: int | None = None) -> Dict[str, Any]:
        """Ejecuta la simulación hasta que todos los drones se detengan o
        hasta alcanzar max_steps si se especifica.
        Devuelve un diccionario con el reporte final.
        """
        pasos = 0
        if max_steps is None:
            while not self.terminada():
                self.step()
                pasos += 1
        else:
            while not self.terminada() and pasos < max_steps:
                self.step()
                pasos += 1
        if pasos == 0:
            self.datacollector.collect(self)
        return self.generar_reporte(pasos)

class Obstaculo(Agent):
    def __init__(self, unique_id, model, pos, tipo):
        super().__init__(unique_id, model)
        self.tipo = tipo


