import sqlite3
from Graph import Graph
from Node import Node
from Edge import Edge

def cargar_grafo_desde_bd(db_path="rutas.db"):
    """
    Carga los datos de ciudades y enlaces desde la base de datos y construye el grafo.
    
    Args:
        db_path (str): Ruta al archivo de base de datos SQLite.
    
    Returns:
        Graph: Grafo construido con nodos y aristas.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    grafo = Graph()

    # Cargar ciudades
    cursor.execute("SELECT rowid, nombre FROM Ciudad")
    ciudad_id_map = {}  # Mapear ID a nombre
    for row in cursor.fetchall():
        ciudad_id, nombre = row
        ciudad_id_map[ciudad_id] = nombre
        grafo.add_or_get_node(nombre)

    # Cargar enlaces
    cursor.execute("SELECT idOrigen, idDestino, saturacion, tiempo, animales FROM Enlace")
    for row in cursor.fetchall():
        id_origen, id_destino, saturacion, tiempo, animales = row
        nombre_origen = ciudad_id_map.get(id_origen)
        nombre_destino = ciudad_id_map.get(id_destino)
        if nombre_origen and nombre_destino:
            grafo.add_edge(nombre_origen, nombre_destino, saturacion, tiempo, animales)

    conn.close()
    return grafo
