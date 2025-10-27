class Edge:
    """
    Representa una ruta aérea entre dos ciudades (nodos) con factores que afectan su peso:
    saturación del tráfico, tiempo de vuelo y riesgo por animales.
    """

    def __init__(self, destination_node, saturacion, tiempo, animales):
        """
        Inicializa una arista con los factores que afectan el peso.
        
        Args:
            destination_node (Node): Ciudad destino.
            saturacion (float): Nivel de tráfico aéreo.
            tiempo (float): Tiempo estimado de vuelo.
            animales (float): Riesgo por fauna aérea.
        """
        self.destination = destination_node
        self.saturacion = saturacion
        self.tiempo = tiempo
        self.animales = animales

    def calcular_peso(self):
        """
        Calcula el peso total de la ruta según los factores.
        
        Returns:
            float: Peso total.
        """
        return self.saturacion * 2 + self.tiempo + self.animales * 3

    def update(self, saturacion, tiempo, animales):
        """
        Actualiza los valores de la arista.
        """
        self.saturacion = saturacion
        self.tiempo = tiempo
        self.animales = animales

    def get_destination(self):
        """
        Devuelve el nodo de destino.
        
        Returns:
            Node: Nodo destino.
        """
        return self.destination
