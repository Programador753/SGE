class Edge:
    """
    Clase Edge que representa una arista entre dos nodos en un grafo,
    con un peso asociado que puede incrementarse o disminuirse.
    """

    def __init__(self, destination_node):
        """
        Inicializa una arista con un nodo de destino y peso inicial de 1.
        
        Args:
            destination_node (Node): Nodo al que apunta esta arista.
        """
        self.destination = destination_node  # Nodo al que apunta la arista
        self.weight = 1  # Peso inicial de la arista (frecuencia de aparición)

    def increment_weight(self):
        """
        Incrementa el peso de la arista en 1 (aumenta la frecuencia).
        """
        self.weight += 1

    def get_destination(self):
        """
        Obtiene el nodo de destino de esta arista.
        
        Returns:
            Node: El nodo de destino.
        """
        return self.destination

    def get_weight(self):
        """
        Obtiene el peso actual de la arista.
        
        Returns:
            int: El peso de la arista.
        """
        return self.weight