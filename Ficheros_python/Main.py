import os
from Graph import Graph


def main():
    """
    Función principal que carga archivos de texto en un grafo y genera una "canción"
    a partir de las conexiones entre palabras.
    
    Crea un grafo con palabras de múltiples archivos de texto, y luego genera
    una secuencia de palabras basada en las conexiones del grafo.
    """
    # Crear una instancia del grafo
    print("=" * 70)
    print("SISTEMA DE GENERACIÓN DE TEXTO BASADO EN GRAFOS PONDERADOS")
    print("=" * 70)
    print()
    
    graph = Graph()
    
    # Definir la carpeta donde están las canciones
    songs_folder = "Canciones"
    
    # Verificar que la carpeta existe
    if not os.path.exists(songs_folder):
        print(f"Error: La carpeta '{songs_folder}' no existe.")
        return
    
    # Cargar todos los archivos .txt de la carpeta
    print("Fase 1: Cargando y procesando archivos de canciones...")
    print("-" * 70)
    
    song_files = [f for f in os.listdir(songs_folder) if f.endswith('.txt')]
    
    if not song_files:
        print(f"Error: No se encontraron archivos .txt en la carpeta '{songs_folder}'.")
        return
    
    # Procesar cada archivo de canción
    for i, filename in enumerate(sorted(song_files), 1):
        filepath = os.path.join(songs_folder, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                text = file.read()
                graph.load_text(text)
                print(f"  [{i}/{len(song_files)}] Cargado: {filename}")
        except Exception as e:
            print(f"  Error al cargar {filename}: {e}")
    
    print()
    print("Fase 2: Construcción del grafo completada")
    print("-" * 70)
    graph.display_graph_info()
    
    print()
    print("Fase 3: Generando secuencia de texto...")
    print("-" * 70)
    
    # Generar una secuencia de 300 palabras
    generated_text = graph.generate_sequence(300)
    
    print()
    print("TEXTO GENERADO:")
    print("=" * 70)
    print(generated_text)
    print("=" * 70)
    
    # Guardar el resultado en un archivo
    output_file = "cancion_generada.txt"
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("TEXTO GENERADO POR EL SISTEMA DE GRAFOS PONDERADOS\n")
            file.write("=" * 70 + "\n\n")
            file.write(generated_text)
            file.write("\n\n" + "=" * 70 + "\n")
        print()
        print(f"El texto generado se ha guardado en: {output_file}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")


if __name__ == "__main__":
    main()
