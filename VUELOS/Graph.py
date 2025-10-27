from Node import Node  # Clase que representa una ciudad (nodo)
from Edge import Edge  # Clase que representa un enlace (arista)

class Graph:
    """
    Clase Graph que representa un grafo dirigido de ciudades conectadas por rutas aéreas.
    Permite añadir nodos (ciudades), añadir aristas (enlaces), y consultar información del grafo.
    """

    def __init__(self):
        self.nodes = []  # Lista de nodos únicos

    def find_node(self, name):
        """
        Busca un nodo por su nombre (contenido).
        
        Args:
            name (str): Nombre de la ciudad.
        
        Returns:
            Node: Nodo encontrado o None.
        """
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def add_or_get_node(self, name):
        """
        Añade un nodo si no existe, o lo devuelve si ya está en el grafo.
        
        Args:
            name (str): Nombre de la ciudad.
        
        Returns:
            Node: Nodo correspondiente.
        """
        node = self.find_node(name)
        if node:
            return node
        new_node = Node(name)
        self.nodes.append(new_node)
        return new_node

    def add_edge(self, from_name, to_name, saturacion, tiempo, animales):
        """
        Añade una arista entre dos nodos con los parámetros de peso.
        
        Args:
            from_name (str): Ciudad origen.
            to_name (str): Ciudad destino.
            saturacion (float): Nivel de tráfico aéreo.
            tiempo (float): Tiempo estimado de vuelo.
            animales (float): Riesgo por fauna aérea.
        """
        from_node = self.add_or_get_node(from_name)
        to_node = self.add_or_get_node(to_name)

        existing_edge = from_node.find_edge(to_node)
        if existing_edge:
            # Actualiza los valores si ya existe
            existing_edge.update(saturacion, tiempo, animales)
        else:
            # Crea una nueva arista
            new_edge = Edge(to_node, saturacion, tiempo, animales)
            from_node.add_edge(new_edge)

    def get_neighbors(self, node):
        """
        Devuelve los vecinos (nodos conectados) de un nodo.
        
        Args:
            node (Node): Nodo origen.
        
        Returns:
            List[Edge]: Lista de aristas salientes.
        """
        return node.edges

    def display_graph_info(self):
        """
        Muestra estadísticas del grafo.
        """
        print(f"🔹 Total de ciudades: {len(self.nodes)}")
        total_edges = sum(len(node.edges) for node in self.nodes)
        print(f"🔹 Total de rutas aéreas: {total_edges}")
        if self.nodes:
            max_edges = max(len(node.edges) for node in self.nodes)
            print(f"🔹 Máximo de rutas desde una ciudad: {max_edges}")
