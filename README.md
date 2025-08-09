# Optimización del Tráfico de Drones de Entrega en Zonas Urbanas Densas

Este proyecto simula el tráfico de drones de entrega en una ciudad usando el framework Mesa y NetworkX. Permite comparar los algoritmos de ruta Dijkstra y A\*, analizar colisiones y optimizar rutas en diferentes escenarios de densidad.

## Estructura del Proyecto

-   `modelo_ciudad.py`: Lógica del modelo, obstáculos, métricas.
-   `agente_dron.py`: Agente dron, navegación, colisiones.
-   `servidor_visual.py`: Servidor web y visualización interactiva.

## Instalación

Este proyecto está probado con Mesa 1.1.0 y Python 3.10. Recomendado usar un entorno virtual con Python 3.10 y las dependencias fijadas en `requirements.txt`.

-   Bash/Zsh:

    ```bash
    python3.10 -m venv venv310
    source venv310/bin/activate
    pip install -U pip
    pip install -r requirements.txt
    ```

-   Fish:

    ```fish
    python3.10 -m venv venv310
    source venv310/bin/activate.fish
    pip install -U pip
    pip install -r requirements.txt
    ```

## Ejecución

```bash
python servidor_visual.py
```

Luego abre http://localhost:8521 en tu navegador.

## Ejecución sin interfaz (reporte JSON)

Para correr hasta que la simulación termine (cuando todos los drones se detienen) y obtener un reporte para tomar decisiones:

```bash
python run_headless.py
```

El reporte incluye parámetros del modelo, resultados (entregas, tasa de entrega, colisiones, desvíos, fallas de batería, drones bloqueados, tiempos de entrega) y recomendaciones accionables basadas en los datos.

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
