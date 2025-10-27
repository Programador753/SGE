class Node:
    """
    Representa una ciudad en el grafo, con una lista de rutas aéreas (aristas) hacia otras ciudades.
    """

    def __init__(self, name):
        """
        Inicializa una ciudad con su nombre y una lista vacía de rutas salientes.
        
        Args:
            name (str): Nombre de la ciudad.
        """
        self.name = name
        self.edges = []  # Lista de objetos Edge (rutas aéreas)

    def add_edge(self, edge):
        """
        Añade una ruta aérea (arista) desde esta ciudad hacia otra.
        
        Args:
            edge (Edge): Ruta aérea a añadir.
        """
        self.edges.append(edge)

    def find_edge(self, destination_node):
        """
        Busca una ruta aérea que conecte esta ciudad con otra ciudad destino.
        
        Args:
            destination_node (Node): Ciudad destino.
        
        Returns:
            Edge: Ruta encontrada o None.
        """
        for edge in self.edges:
            if edge.destination == destination_node:
                return edge
        return None

    def has_edges(self):
        """
        Verifica si esta ciudad tiene rutas aéreas salientes.
        
        Returns:
            bool: True si tiene rutas, False si no.
        """
        return len(self.edges) > 0

    def get_neighbors(self):
        """
        Devuelve las ciudades conectadas directamente desde esta ciudad.
        
        Returns:
            List[Node]: Lista de ciudades destino.
        """
        return [edge.destination for edge in self.edges]

    def __str__(self):
        return f"Ciudad({self.name})"
