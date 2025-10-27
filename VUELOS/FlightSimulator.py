from DijkstraSolver import DijkstraSolver

class FlightSimulator:
    """
    Simula el vuelo de un avión entre dos ciudades, recalculando la ruta en cada paso.
    Permite detectar cambios en las condiciones y adaptar la ruta dinámicamente.
    """

    def __init__(self, graph, origin_name, destination_name):
        self.graph = graph
        self.origin = graph.find_node(origin_name)
        self.destination = graph.find_node(destination_name)
        self.solver = DijkstraSolver(graph)
        self.route = self.solver.find_shortest_path(self.origin, self.destination)
        self.position = 0
        self.route_changes = 0  # Contador de cambios de ruta

    def advance(self):
        """
        Avanza el avión a la siguiente ciudad en la ruta. Recalcula si cambian las condiciones.
        """
        if self.position >= len(self.route) - 1:
            print("\nEl avión ha llegado a su destino.")
            print(f"Cambios de ruta durante el vuelo: {self.route_changes}")
            return False

        current = self.route[self.position]
        next_node = self.route[self.position + 1]
        
        # Calcular peso del enlace actual
        edge = current.find_edge(next_node)
        peso_actual = edge.calcular_peso() if edge else "N/A"
        
        print(f"\nVolando de {current.name} a {next_node.name}")
        print(f"   Peso de la ruta: {peso_actual:.2f}")
        input("   Pulsa Enter para continuar...")

        self.position += 1

        # Recalcular ruta desde la nueva posición
        if self.position < len(self.route) - 1:
            new_route = self.solver.find_shortest_path(self.route[self.position], self.destination)
            old_route_names = [node.name for node in self.route[self.position:]]
            new_route_names = [node.name for node in new_route]
            
            if new_route_names != old_route_names:
                print("\nRECALCULANDO RUTA!")
                print(f"   Ruta anterior: {' -> '.join(old_route_names)}")
                print(f"   Nueva ruta: {' -> '.join(new_route_names)}")
                self.route = self.route[:self.position] + new_route
                self.route_changes += 1

        return True
    
    def get_current_position(self):
        """Devuelve la posición actual del avión."""
        if self.position < len(self.route):
            return self.route[self.position]
        return None
    
    def get_route_info(self):
        """Devuelve información sobre la ruta actual."""
        return {
            'route': [node.name for node in self.route],
            'position': self.position,
            'current_city': self.route[self.position].name if self.position < len(self.route) else None,
            'destination': self.destination.name,
            'completed': self.position >= len(self.route) - 1,
            'route_changes': self.route_changes
        }
