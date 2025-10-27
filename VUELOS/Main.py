from Graph import Graph
from FlightSimulator import FlightSimulator
from cargar_grafo_desde_bd import cargar_grafo_desde_bd


# Cargar grafo desde base de datos
graph = cargar_grafo_desde_bd()

# Mostrar ciudades disponibles
for node in graph.nodes:
    print(f"- {node.name}")

# Pedir origen y destino
origen = input("Ciudad origen: ")
destino = input("Ciudad destino: ")

# Iniciar simulador
simulador = FlightSimulator(graph, origen, destino)
while simulador.advance():
    pass
