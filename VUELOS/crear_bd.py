import sqlite3
import random

def crear_y_poblar_bd():
    conn = sqlite3.connect("rutas.db")
    cursor = conn.cursor()
    
    # Semilla para reproducibilidad (opcional)
    random.seed(42)

    # Eliminar tablas si ya existen
    cursor.execute("DROP TABLE IF EXISTS Ciudad")
    cursor.execute("DROP TABLE IF EXISTS Enlace")

    # Crear tabla Ciudad
    cursor.execute("""
        CREATE TABLE Ciudad (
            nombre TEXT,
            poblacion INTEGER,
            km2 REAL
        )
    """)

    # Crear tabla Enlace
    cursor.execute("""
        CREATE TABLE Enlace (
            idOrigen INTEGER,
            idDestino INTEGER,
            saturacion REAL,
            tiempo REAL,
            animales REAL
        )
    """)

    # Insertar ciudades (expandido a 15 ciudades)
    ciudades = [
        ('Madrid', 3266000, 604.3),
        ('Barcelona', 1620000, 101.9),
        ('Valencia', 794000, 134.6),
        ('Sevilla', 688000, 140.8),
        ('Bilbao', 345000, 41.5),
        ('Zaragoza', 675000, 973.8),
        ('Málaga', 578000, 398.0),
        ('Granada', 232000, 88.0),
        ('Alicante', 337000, 201.3),
        ('San Sebastián', 188000, 60.9),
        ('Murcia', 453000, 881.9),
        ('Palma', 416000, 208.6),
        ('Valladolid', 298000, 197.9),
        ('Córdoba', 325000, 1255.2),
        ('Vigo', 295000, 109.1)
    ]
    cursor.executemany("INSERT INTO Ciudad (nombre, poblacion, km2) VALUES (?, ?, ?)", ciudades)

    # Insertar enlaces (rutas entre ciudades) - RED MUCHO MAS DENSA
    # Ahora cada ciudad tiene multiples conexiones, creando muchas rutas alternativas
    # Se agrega un pequeño factor aleatorio para evitar empates
    enlaces_base = [
        # Desde Madrid (id=1) - hub principal
        (1, 2, 0.7, 1.2, 0.1),   # Madrid -> Barcelona
        (1, 3, 0.6, 1.0, 0.2),   # Madrid -> Valencia
        (1, 4, 0.5, 1.3, 0.1),   # Madrid -> Sevilla
        (1, 5, 0.6, 1.5, 0.2),   # Madrid -> Bilbao
        (1, 6, 0.4, 0.9, 0.1),   # Madrid -> Zaragoza
        (1, 7, 0.3, 1.6, 0.2),   # Madrid -> Málaga
        (1, 13, 0.5, 0.8, 0.1),  # Madrid -> Valladolid
        
        # Desde Barcelona (id=2) - hub importante
        (2, 1, 0.7, 1.2, 0.1),   # Barcelona -> Madrid
        (2, 3, 0.5, 1.0, 0.2),   # Barcelona -> Valencia
        (2, 6, 0.4, 0.8, 0.1),   # Barcelona -> Zaragoza
        (2, 10, 0.7, 1.5, 0.3),  # Barcelona -> San Sebastián
        (2, 5, 0.6, 1.4, 0.2),   # Barcelona -> Bilbao
        (2, 12, 0.5, 0.6, 0.1),  # Barcelona -> Palma
        
        # Desde Valencia (id=3)
        (3, 1, 0.6, 1.0, 0.2),   # Valencia -> Madrid
        (3, 2, 0.5, 1.0, 0.2),   # Valencia -> Barcelona
        (3, 4, 0.6, 1.5, 0.3),   # Valencia -> Sevilla
        (3, 6, 0.5, 1.4, 0.2),   # Valencia -> Zaragoza
        (3, 9, 0.4, 0.5, 0.1),   # Valencia -> Alicante
        (3, 11, 0.5, 0.8, 0.2),  # Valencia -> Murcia
        (3, 12, 0.6, 0.7, 0.1),  # Valencia -> Palma
        
        # Desde Sevilla (id=4)
        (4, 1, 0.5, 1.3, 0.1),   # Sevilla -> Madrid
        (4, 3, 0.6, 1.5, 0.3),   # Sevilla -> Valencia
        (4, 5, 0.4, 1.3, 0.1),   # Sevilla -> Bilbao
        (4, 7, 0.5, 0.8, 0.2),   # Sevilla -> Málaga
        (4, 8, 0.4, 0.9, 0.1),   # Sevilla -> Granada
        (4, 9, 0.6, 1.1, 0.1),   # Sevilla -> Alicante
        (4, 14, 0.3, 0.4, 0.1),  # Sevilla -> Córdoba
        
        # Desde Bilbao (id=5)
        (5, 1, 0.6, 1.5, 0.2),   # Bilbao -> Madrid
        (5, 2, 0.6, 1.4, 0.2),   # Bilbao -> Barcelona
        (5, 6, 0.8, 1.1, 0.2),   # Bilbao -> Zaragoza
        (5, 10, 0.3, 0.4, 0.1),  # Bilbao -> San Sebastián
        (5, 13, 0.5, 0.9, 0.1),  # Bilbao -> Valladolid
        (5, 15, 0.6, 1.2, 0.2),  # Bilbao -> Vigo
        
        # Desde Zaragoza (id=6) - hub intermedio
        (6, 1, 0.4, 0.9, 0.1),   # Zaragoza -> Madrid
        (6, 2, 0.4, 0.8, 0.1),   # Zaragoza -> Barcelona
        (6, 3, 0.5, 1.4, 0.2),   # Zaragoza -> Valencia
        (6, 5, 0.8, 1.1, 0.2),   # Zaragoza -> Bilbao
        (6, 13, 0.5, 0.7, 0.1),  # Zaragoza -> Valladolid
        
        # Desde Málaga (id=7)
        (7, 1, 0.3, 1.6, 0.2),   # Málaga -> Madrid
        (7, 4, 0.5, 0.8, 0.2),   # Málaga -> Sevilla
        (7, 8, 0.5, 1.2, 0.1),   # Málaga -> Granada
        (7, 14, 0.4, 0.6, 0.1),  # Málaga -> Córdoba
        
        # Desde Granada (id=8)
        (8, 4, 0.4, 0.9, 0.1),   # Granada -> Sevilla
        (8, 7, 0.5, 1.2, 0.1),   # Granada -> Málaga
        (8, 9, 0.6, 1.0, 0.2),   # Granada -> Alicante
        (8, 11, 0.5, 0.9, 0.1),  # Granada -> Murcia
        (8, 14, 0.4, 0.5, 0.1),  # Granada -> Córdoba
        
        # Desde Alicante (id=9)
        (9, 3, 0.4, 0.5, 0.1),   # Alicante -> Valencia
        (9, 4, 0.6, 1.1, 0.1),   # Alicante -> Sevilla
        (9, 8, 0.6, 1.0, 0.2),   # Alicante -> Granada
        (9, 10, 0.4, 1.3, 0.1),  # Alicante -> San Sebastián
        (9, 11, 0.3, 0.4, 0.1),  # Alicante -> Murcia
        (9, 12, 0.5, 0.6, 0.1),  # Alicante -> Palma
        
        # Desde San Sebastián (id=10)
        (10, 2, 0.7, 1.5, 0.3),  # San Sebastián -> Barcelona
        (10, 5, 0.3, 0.4, 0.1),  # San Sebastián -> Bilbao
        (10, 9, 0.4, 1.3, 0.1),  # San Sebastián -> Alicante
        (10, 15, 0.5, 1.0, 0.2), # San Sebastián -> Vigo
        
        # Desde Murcia (id=11)
        (11, 3, 0.5, 0.8, 0.2),  # Murcia -> Valencia
        (11, 8, 0.5, 0.9, 0.1),  # Murcia -> Granada
        (11, 9, 0.3, 0.4, 0.1),  # Murcia -> Alicante
        (11, 12, 0.6, 0.8, 0.2), # Murcia -> Palma
        
        # Desde Palma (id=12)
        (12, 2, 0.5, 0.6, 0.1),  # Palma -> Barcelona
        (12, 3, 0.6, 0.7, 0.1),  # Palma -> Valencia
        (12, 9, 0.5, 0.6, 0.1),  # Palma -> Alicante
        (12, 11, 0.6, 0.8, 0.2), # Palma -> Murcia
        
        # Desde Valladolid (id=13)
        (13, 1, 0.5, 0.8, 0.1),  # Valladolid -> Madrid
        (13, 5, 0.5, 0.9, 0.1),  # Valladolid -> Bilbao
        (13, 6, 0.5, 0.7, 0.1),  # Valladolid -> Zaragoza
        (13, 15, 0.4, 0.8, 0.1), # Valladolid -> Vigo
        
        # Desde Córdoba (id=14)
        (14, 4, 0.3, 0.4, 0.1),  # Córdoba -> Sevilla
        (14, 7, 0.4, 0.6, 0.1),  # Córdoba -> Málaga
        (14, 8, 0.4, 0.5, 0.1),  # Córdoba -> Granada
        (14, 1, 0.6, 1.2, 0.2),  # Córdoba -> Madrid
        
        # Desde Vigo (id=15)
        (15, 5, 0.6, 1.2, 0.2),  # Vigo -> Bilbao
        (15, 10, 0.5, 1.0, 0.2), # Vigo -> San Sebastián
        (15, 13, 0.4, 0.8, 0.1), # Vigo -> Valladolid
        (15, 1, 0.7, 1.4, 0.2),  # Vigo -> Madrid
    ]
    
    # Agregar variación aleatoria pequeña para evitar empates
    enlaces = []
    for origen, destino, sat, tiempo, anim in enlaces_base:
        # Agregar variación de +/- 0.001 a 0.01 en cada parámetro
        sat_var = sat + random.uniform(-0.01, 0.01)
        tiempo_var = tiempo + random.uniform(-0.01, 0.01)
        anim_var = anim + random.uniform(-0.005, 0.005)
        
        # Asegurar que estén en rangos válidos
        sat_var = max(0.01, min(0.99, sat_var))
        tiempo_var = max(0.1, min(3.0, tiempo_var))
        anim_var = max(0.01, min(0.99, anim_var))
        
        enlaces.append((origen, destino, sat_var, tiempo_var, anim_var))
    
    cursor.executemany("INSERT INTO Enlace (idOrigen, idDestino, saturacion, tiempo, animales) VALUES (?, ?, ?, ?, ?)", enlaces)

    conn.commit()
    conn.close()
    print("✅ Base de datos creada y poblada con éxito.")

if __name__ == "__main__":
    crear_y_poblar_bd()
