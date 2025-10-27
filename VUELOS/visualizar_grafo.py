"""
Programa para visualizar el grafo de rutas aéreas.
Muestra las ciudades (nodos) y las conexiones con sus pesos.
"""

import matplotlib.pyplot as plt
import networkx as nx
from cargar_grafo_desde_bd import cargar_grafo_desde_bd


def visualizar_grafo(graph):
    """
    Crea una visualización del grafo mostrando nodos, aristas y pesos.
    
    Args:
        graph (Graph): Grafo a visualizar.
    """
    # Crear un grafo dirigido de NetworkX
    G = nx.DiGraph()
    
    # Añadir nodos
    for node in graph.nodes:
        G.add_node(node.name)
    
    # Añadir aristas con sus pesos
    edge_labels = {}
    for node in graph.nodes:
        for edge in node.edges:
            peso = edge.calcular_peso()
            G.add_edge(node.name, edge.destination.name, weight=peso)
            # Guardar la etiqueta solo con el peso
            edge_key = (node.name, edge.destination.name)
            edge_labels[edge_key] = f'{peso:.2f}'
    
    # Configurar el diseño del grafo
    plt.figure(figsize=(16, 12))
    
    # Usar diferentes layouts según la cantidad de nodos
    if len(graph.nodes) <= 10:
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    else:
        pos = nx.kamada_kawai_layout(G)
    
    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, 
                          node_color='lightblue', 
                          node_size=3000,
                          alpha=0.9)
    
    # Dibujar etiquetas de nodos
    nx.draw_networkx_labels(G, pos, 
                           font_size=10, 
                           font_weight='bold')
    
    # Dibujar aristas con flechas
    nx.draw_networkx_edges(G, pos, 
                          edge_color='gray',
                          arrows=True,
                          arrowsize=20,
                          arrowstyle='->',
                          connectionstyle='arc3,rad=0.1',
                          width=2,
                          alpha=0.6)
    
    # Dibujar etiquetas de aristas
    nx.draw_networkx_edge_labels(G, pos, 
                                 edge_labels,
                                 font_size=9,
                                 font_color='darkred',
                                 font_weight='bold',
                                 bbox=dict(boxstyle='round,pad=0.2', 
                                          facecolor='yellow', 
                                          edgecolor='black',
                                          alpha=0.9))
    
    plt.title("Grafo de Rutas Aéreas\n(Peso total = Saturación×2 + Tiempo + Animales×3)", 
             fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    
    # Guardar la imagen
    plt.savefig('grafo_rutas.png', dpi=300, bbox_inches='tight')
    print("\n✓ Imagen guardada como 'grafo_rutas.png'")
    
    # Mostrar el grafo
    plt.show()


def mostrar_informacion_grafo(graph):
    """
    Muestra información detallada del grafo en formato texto.
    
    Args:
        graph (Graph): Grafo a analizar.
    """
    print("\n" + "="*80)
    print("INFORMACIÓN DEL GRAFO DE RUTAS AÉREAS")
    print("="*80)
    
    print(f"\nCiudades totales: {len(graph.nodes)}")
    print(f"\nLista de ciudades:")
    for i, node in enumerate(graph.nodes, 1):
        print(f"  {i}. {node.name}")
    
    print("\n" + "-"*80)
    print("RUTAS Y PESOS DETALLADOS:")
    print("-"*80)
    
    total_rutas = 0
    for node in graph.nodes:
        if node.has_edges():
            print(f"\nDesde {node.name}:")
            for edge in node.edges:
                peso = edge.calcular_peso()
                total_rutas += 1
                print(f"  → {edge.destination.name}")
                print(f"     Saturación: {edge.saturacion} | Tiempo: {edge.tiempo} | Animales: {edge.animales}")
                print(f"     Peso total: {peso:.2f} (S×2 + T + A×3 = {edge.saturacion}×2 + {edge.tiempo} + {edge.animales}×3)")
    
    print(f"\n{'-'*80}")
    print(f"Total de rutas: {total_rutas}")
    print("="*80)


def main():
    """
    Función principal que carga y visualiza el grafo.
    """
    print("Cargando grafo desde la base de datos...")
    graph = cargar_grafo_desde_bd()
    
    if not graph or not graph.nodes:
        print("❌ Error: No se pudo cargar el grafo o está vacío.")
        return
    
    print(f"✓ Grafo cargado con {len(graph.nodes)} ciudades")
    
    # Mostrar información en texto
    mostrar_informacion_grafo(graph)
    
    # Generar visualización gráfica directamente
    print("\nGenerando visualización del grafo...")
    try:
        visualizar_grafo(graph)
    except ImportError as e:
        print(f"\n❌ Error: Falta instalar las librerías necesarias.")
        print("Ejecuta: pip install matplotlib networkx")
    except Exception as e:
        print(f"\n❌ Error al visualizar el grafo: {e}")


if __name__ == "__main__":
    main()
