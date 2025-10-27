import random
import string
from Node import Node  # Clase para representar un nodo en el grafo
from Edge import Edge  # Clase para representar una arista entre dos nodos

class Graph:
    """
    Clase Graph que representa un grafo dirigido. Permite la creación de nodos,
    la adición de aristas entre nodos, y la visualización de los nodos en el grafo.
    """

    def __init__(self):
        """
        Inicializa un grafo vacío.
        """
        self.nodes = []

    def find_node(self, content):
        """
        Busca un nodo en el grafo según su contenido.
        
        Args:
            content (str): El contenido del nodo a buscar.
            
        Returns:
            Node: El nodo encontrado, o None si no existe.
        """
        for node in self.nodes:
            if node.get_content() == content:
                return node
        return None

    def add_or_get_node(self, content):
        """
        Busca un nodo con el contenido especificado. Si no existe, lo crea.
        
        Args:
            content (str): Contenido del nodo.
            
        Returns:
            Node: El nodo encontrado o recién creado.
        """
        existing_node = self.find_node(content)
        if existing_node:
            return existing_node
        
        # Si no existe, crear un nuevo nodo y añadirlo al grafo
        new_node = Node(content)
        self.nodes.append(new_node)
        return new_node

    def add_edge(self, from_content, to_content):
        """
        Añade o actualiza una arista entre dos nodos especificados por su contenido.
        Si la arista ya existe, incrementa su peso. Si no existe, la crea.
        
        Args:
            from_content (str): Contenido del nodo de origen.
            to_content (str): Contenido del nodo de destino.
        """
        # Obtener o crear los nodos de origen y destino
        from_node = self.add_or_get_node(from_content)
        to_node = self.add_or_get_node(to_content)
        
        # Buscar si ya existe una arista entre estos nodos
        existing_edge = from_node.find_edge(to_node)
        
        if existing_edge:
            # Si existe, incrementar su peso
            existing_edge.increment_weight()
        else:
            # Si no existe, crear una nueva arista
            new_edge = Edge(to_node)
            from_node.add_edge(new_edge)

    def preprocess_text(self, text):
        """
        Normaliza el texto: convierte a minúsculas y elimina signos de puntuación.
        
        Args:
            text (str): Texto a procesar.
            
        Returns:
            list: Lista de palabras limpias.
        """
        # Convertir a minúsculas
        text = text.lower()
        
        # Eliminar signos de puntuación
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)
        
        # Dividir en palabras y eliminar espacios extra
        words = text.split()
        
        return words

    def load_text(self, text):
        """
        Procesa un texto completo y construye el grafo con las relaciones entre palabras.
        
        Args:
            text (str): Texto a cargar en el grafo.
        """
        # Preprocesar el texto para obtener las palabras limpias
        words = self.preprocess_text(text)
        
        # Crear aristas entre palabras consecutivas
        for i in range(len(words) - 1):
            current_word = words[i]
            next_word = words[i + 1]
            self.add_edge(current_word, next_word)

    def generate_sequence(self, length=300, max_repetitions=2):
        """
        Genera una secuencia de palabras recorriendo el grafo de manera codiciosa.
        Selecciona en cada paso la arista con mayor peso, evitando bucles infinitos
        mediante el seguimiento de nodos visitados recientemente.
        
        Args:
            length (int): Número de palabras a generar.
            max_repetitions (int): Número máximo de veces que se permite repetir
                                   la misma palabra consecutivamente antes de forzar
                                   un cambio.
            
        Returns:
            str: Texto generado.
        """
        if not self.nodes:
            return "El grafo está vacío."
        
        # Seleccionar un nodo inicial aleatorio
        current_node = random.choice(self.nodes)
        sequence = [current_node.get_content()]
        
        # Mantener un historial de los últimos nodos visitados para detectar ciclos
        recent_nodes = [current_node]
        max_history = 10  # Tamaño del historial para detectar ciclos
        
        # Generar la secuencia
        for _ in range(length - 1):
            if not current_node.has_edges():
                # Si el nodo actual no tiene aristas salientes, seleccionar uno aleatorio
                current_node = random.choice(self.nodes)
                sequence.append(current_node.get_content())
                recent_nodes.append(current_node)
            else:
                # Contar repeticiones consecutivas de la misma palabra
                consecutive_count = 1
                for i in range(len(sequence) - 1, -1, -1):
                    if sequence[i] == current_node.get_content():
                        consecutive_count += 1
                    else:
                        break
                
                # Si hay demasiadas repeticiones, forzar un salto aleatorio
                if consecutive_count >= max_repetitions:
                    current_node = random.choice(self.nodes)
                    sequence.append(current_node.get_content())
                    recent_nodes.append(current_node)
                else:
                    # Obtener la arista con mayor peso
                    max_edge = current_node.get_max_weight_edge()
                    next_node = max_edge.get_destination()
                    
                    # Detectar ciclos: si el siguiente nodo está en el historial reciente
                    # con alta frecuencia, considerar una alternativa
                    recent_count = recent_nodes[-max_history:].count(next_node)
                    
                    if recent_count >= 3 and len(current_node.edges) > 1:
                        # Intentar elegir una arista alternativa
                        alternative_edges = [edge for edge in current_node.edges 
                                           if edge.get_destination() not in recent_nodes[-5:]]
                        if alternative_edges:
                            # Elegir aleatoriamente entre las alternativas
                            selected_edge = random.choice(alternative_edges)
                            next_node = selected_edge.get_destination()
                    
                    current_node = next_node
                    sequence.append(current_node.get_content())
                    recent_nodes.append(current_node)
            
            # Mantener el historial de tamaño limitado
            if len(recent_nodes) > max_history:
                recent_nodes.pop(0)
        
        # Unir las palabras en un texto
        return ' '.join(sequence)

    def display_graph_info(self):
        """
        Muestra información básica sobre el grafo (número de nodos).
        """
        print(f"El grafo contiene {len(self.nodes)} nodos únicos (palabras).")
        
        # Mostrar algunas estadísticas adicionales
        total_edges = sum(len(node.edges) for node in self.nodes)
        print(f"Total de conexiones (aristas): {total_edges}")
        
        if self.nodes:
            max_connections = max(len(node.edges) for node in self.nodes)
            print(f"Máximo de conexiones desde un nodo: {max_connections}")
