import heapq

class DijkstraSolver:
    """
    Implementa el algoritmo de Dijkstra para encontrar la ruta más ligera entre dos ciudades.
    """

    def __init__(self, graph):
        self.graph = graph
        self.counter = 0  # Contador para desempatar en el heap

    def find_shortest_path(self, origin_node, destination_node):
        distances = {node: float('inf') for node in self.graph.nodes}
        previous = {node: None for node in self.graph.nodes}
        distances[origin_node] = 0

        # Usar contador para evitar comparaciones entre nodos
        queue = [(0, self.counter, origin_node)]
        self.counter += 1

        while queue:
            current_dist, _, current_node = heapq.heappop(queue)

            if current_node == destination_node:
                break

            # Skip si ya procesamos un camino mejor
            if current_dist > distances[current_node]:
                continue

            for edge in current_node.edges:
                neighbor = edge.destination
                weight = edge.calcular_peso()
                new_dist = current_dist + weight

                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current_node
                    heapq.heappush(queue, (new_dist, self.counter, neighbor))
                    self.counter += 1

        # Reconstruir ruta
        path = []
        current = destination_node
        while current:
            path.insert(0, current)
            current = previous[current]

        return path
