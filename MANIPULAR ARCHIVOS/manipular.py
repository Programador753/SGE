print("--- LEYENDO EL INVENTARIO ---")

with open('inventario.csv', 'r', encoding='utf-8') as archivo:
    # 1. Leemos la primera línea (encabezados) para saltarla
    encabezados = archivo.readline()
    
    valor_total_inventario = 0.0
    
    # 2. Leemos el resto línea por línea
    for linea in archivo:
        linea = linea.strip() # Limpiamos espacios y saltos
        
        if len(linea) > 0: # Solo procesamos si hay texto
            datos = linea.split(',') # Separamos por comas
            
            # Extraemos datos por índice (0=ID, 1=Producto, 2=Precio, 3=Stock)
            producto = datos[1]
            precio = float(datos[2]) # Convertimos texto a decimal
            stock = int(datos[3])    # Convertimos texto a entero
            
            total_producto = precio * stock
            valor_total_inventario += total_producto
            
            print(f"Producto: {producto} | Valor total: ${total_producto:.2f}")

    print("-" * 30)
    print(f"VALOR TOTAL DEL ALMACÉN: ${valor_total_inventario:.2f}")