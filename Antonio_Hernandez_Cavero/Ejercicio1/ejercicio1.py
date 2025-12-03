# Función para calcular la distancia entre dos años considerando la ausencia del año 0
def distancia(x, y):
    if (x < 0 < y) or (y < 0 < x):
        return abs(x - y) - 1
    else:
        return abs(x - y)

# Función para determinar qué año está más cerca del año B
def año_mas_cercano(A, B, C):
    distancia_A_B = distancia(A, B) 
    distancia_C_B = distancia(C, B)
    
    if distancia_A_B < distancia_C_B:
        return A
    elif distancia_C_B < distancia_A_B:
        return C
    else:
        return "EMPATE"
    
# Lectura de datos
A = int(input("Ingrese el año A: "))
B = int(input("Ingrese el año B: "))
C = int(input("Ingrese el año C: "))
# Cálculo y salida del resultado
resultado = año_mas_cercano(A, B, C)
print(resultado)
