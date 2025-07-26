# Optimización del Tráfico de Drones de Entrega en Zonas Urbanas Densas

Este proyecto simula el tráfico de drones de entrega en una ciudad usando el framework Mesa y NetworkX. Permite comparar los algoritmos de ruta Dijkstra y A\*, analizar colisiones y optimizar rutas en diferentes escenarios de densidad.

## Estructura del Proyecto

-   `modelo_ciudad.py`: Lógica del modelo, obstáculos, métricas.
-   `agente_dron.py`: Agente dron, navegación, colisiones.
-   `servidor_visual.py`: Servidor web y visualización interactiva.

## Instalación

```bash
python -m venv venv
source venv/bin/activate
pip install mesa==1.1.0 networkx matplotlib
```

## Ejecución

```bash
python servidor_visual.py
```

Luego abre http://localhost:8521 en tu navegador.

## Descripción

-   Simulación multiagente de drones en malla urbana.
-   Obstáculos y zonas de exclusión (hospital, aeropuerto).
-   Drones con punto de inicio, destino y batería.
-   Algoritmos de ruta: Dijkstra y A\* (seleccionable).
-   Métricas: tiempo promedio de entrega, colisiones, desvíos.
-   Visualización en tiempo real y análisis comparativo.

## Escenarios

-   Baja, media y alta densidad de drones.

## Autor

Desarrollado con Python 3.10, Mesa y NetworkX.
