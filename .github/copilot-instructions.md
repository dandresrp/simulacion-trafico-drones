# Copilot Instructions for proyecto-trafico-drones

## Project Overview

This project simulates drone traffic in a city grid using the Mesa agent-based modeling framework. The main components are:

-   **modelo_ciudad.py**: Defines the `ModeloCiudad` class, which manages the simulation grid, agent scheduling, obstacles (e.g., hospitals, buildings), and data collection.
-   **agente_dron.py**: Implements the `Dron` agent, supporting both A\* and Dijkstra pathfinding using NetworkX. Drones avoid obstacles and can detect collisions.
-   **servidor_visual.py**: Sets up the Mesa web server for interactive simulation, exposing parameters like drone count and algorithm choice.

## Key Patterns & Conventions

-   **Agent Initialization**: Drones are initialized with unique start/destination points and calculate their route at creation.
-   **Obstacles**: Obstacles and exclusion zones are removed from the NetworkX graph before agent placement.
-   **Pathfinding**: Drones use either A\* or Dijkstra, selectable via the web UI (`algoritmo` parameter).
-   **Metrics**: The model tracks collisions, deviations, and delivery times via a Mesa `DataCollector`.
-   **Visualization**: The grid is visualized as a 20x20 canvas; drones are shown as blue circles.

## Developer Workflows

-   **Run the Simulation**: Start the server with:
    ```bash
    python servidor_visual.py
    ```
    Then visit `http://localhost:8521` in your browser.
-   **Dependencies**: Requires `mesa` and `networkx`. Use a virtual environment and install with:
    ```bash
    pip install mesa networkx
    ```
-   **Python Version**: Managed via `mise.toml` (uses the latest Python).

## Project-Specific Advice

-   **Do not place agents on obstacle nodes**; always use `self.G.nodes()` for valid positions.
-   **When adding new agent types or metrics**, update both the model and the visualization server.
-   **For new pathfinding algorithms**, extend the `Dron.calcular_ruta` method and update the UI choices in `servidor_visual.py`.
-   **Avoid hardcoding grid size**; use the `width` and `height` parameters for flexibility.

## Example: Adding a New Obstacle

To add a new exclusion zone, modify the graph in `ModeloCiudad.__init__`:

```python
zona = [(x, y) for x in range(10, 12) for y in range(10, 12)]
self.G.remove_nodes_from(zona)
```

## Key Files

-   modelo_ciudad.py: Model logic, agent placement, obstacles, metrics
-   agente_dron.py: Drone agent, pathfinding, collision logic
-   servidor_visual.py: Web server, UI parameters, visualization
