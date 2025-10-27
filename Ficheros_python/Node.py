class Node:
    """
    Clase Node que representa un nodo en el grafo, con un contenido asociado
    y una lista de aristas que conectan este nodo con otros.
    """

    def __init__(self, content):
        """
        Inicializa un nodo con un contenido y una lista vacía de aristas.
        
        Args:
            content (str): Contenido o valor asociado al nodo.
        """
        self.content = content  # Almacena el valor o contenido del nodo
        self.edges = []  # Lista para almacenar aristas asociadas a este nodo

    def add_edge(self, edge):
        """
        Añade una arista a la lista de aristas del nodo.
        
        Args:
            edge (Edge): La arista a añadir.
        """
        self.edges.append(edge)

    def find_edge(self, destination_node):
        """
        Busca una arista que tenga como destino el nodo especificado.
        
        Args:
            destination_node (Node): El nodo de destino a buscar.
            
        Returns:
            Edge: La arista encontrada, o None si no existe.
        """
        for edge in self.edges:
            if edge.get_destination() == destination_node:
                return edge
        return None

    def get_max_weight_edge(self):
        """
        Obtiene la arista con el mayor peso (más frecuente).
        
        Returns:
            Edge: La arista con mayor peso, o None si no hay aristas.
        """
        if not self.edges:
            return None
        
        max_edge = self.edges[0]
        for edge in self.edges[1:]:
            if edge.get_weight() > max_edge.get_weight():
                max_edge = edge
        return max_edge

    def get_content(self):
        """
        Obtiene el contenido del nodo.
        
        Returns:
            str: El contenido del nodo.
        """
        return self.content

    def has_edges(self):
        """
        Verifica si el nodo tiene aristas salientes.
        
        Returns:
            bool: True si tiene aristas, False en caso contrario.
        """
        return len(self.edges) > 0
