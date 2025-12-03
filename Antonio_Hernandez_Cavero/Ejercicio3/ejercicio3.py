# Definición del número de dígitos
NUM_DIGITOS = 10

def sumar(a, b, suma):
    """
    Suma dos números naturales grandes representados como vectores.
    a, b: vectores de entrada con dígitos en orden natural (índice 0 = dígito más significativo)
    suma: vector de salida donde se almacena el resultado
    """
    acarreo = 0
    
    # Recorremos de derecha a izquierda (desde las unidades hasta el dígito más significativo)
    for i in range(NUM_DIGITOS - 1, -1, -1):
        # Suma los dígitos de la misma posición más el acarreo
        suma_parcial = a[i] + b[i] + acarreo
        
        # El dígito resultante es el resto de dividir entre 10
        suma[i] = suma_parcial % 10
        
        # El acarreo es el cociente de dividir entre 10
        acarreo = suma_parcial // 10
    
    # Si hay acarreo al final, el resultado excede NUM_DIGITOS
    if acarreo > 0:
        raise OverflowError("La suma genera un resultado con más de NUM_DIGITOS cifras")

def multiplicar(a, b, multiplicacion):
    """
    Multiplica dos números naturales grandes representados como vectores.
    a, b: vectores de entrada con dígitos en orden natural (índice 0 = dígito más significativo)
    multiplicacion: vector de salida donde se almacena el resultado
    """
    # Inicializar el resultado a cero
    for i in range(NUM_DIGITOS):
        multiplicacion[i] = 0
    
    # Multiplicación clásica: cada dígito de 'a' se multiplica por cada dígito de 'b'
    # Recorremos de derecha a izquierda
    for i in range(NUM_DIGITOS - 1, -1, -1):
        if a[i] == 0:
            continue
            
        acarreo = 0
        for j in range(NUM_DIGITOS - 1, -1, -1):
            # Calcular la posición del resultado
            pos_resultado = i + j - (NUM_DIGITOS - 1)
            
            if pos_resultado < 0:
                # Si hay algo que multiplicar o acarreo pendiente, hay overflow
                if b[j] != 0 or acarreo > 0:
                    raise OverflowError("La multiplicación genera un resultado con más de NUM_DIGITOS cifras")
                break
            
            # Multiplicar dígitos y sumar al resultado existente más el acarreo
            producto = a[i] * b[j] + multiplicacion[pos_resultado] + acarreo
            
            # Almacenar el dígito resultante
            multiplicacion[pos_resultado] = producto % 10
            
            # Calcular el nuevo acarreo
            acarreo = producto // 10
        
        # Si queda acarreo al final, verificar que cabe
        if acarreo > 0:
            pos = i + 0 - (NUM_DIGITOS - 1) - 1
            while acarreo > 0 and pos >= 0:
                suma_parcial = multiplicacion[pos] + acarreo
                multiplicacion[pos] = suma_parcial % 10
                acarreo = suma_parcial // 10
                pos -= 1
            
            # Si aún queda acarreo, hay overflow
            if acarreo > 0:
                raise OverflowError("La multiplicación genera un resultado con más de NUM_DIGITOS cifras")

# Ejemplo de uso
# a representa 123 (1,2,3 en el vector = centenas, decenas, unidades)
# b representa 45 (4,5 en el vector)
a = [0, 0, 0, 0, 0, 0, 0, 1, 2, 3]  # 123
b = [0, 0, 0, 0, 0, 0, 0, 0, 4, 5]  # 45

suma = [0] * NUM_DIGITOS # Lista para almacenar la suma
multiplicacion = [0] * NUM_DIGITOS # Lista para almacenar la multiplicación

sumar(a, b, suma)
multiplicar(a, b, multiplicacion)

print("Suma:", suma)  # Debería representar 168
print("Multiplicación:", multiplicacion)  # Debería representar 5535
