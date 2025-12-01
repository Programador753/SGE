# --- SCRIPT PARA GENERAR ARCHIVOS DE EJEMPLO ---

# 1. Crear un archivo CSV (inventario.csv)
csv_data = """ID,Producto,Precio,Stock
101,Teclado Mecanico,45.50,15
102,Mouse Gamer,25.00,30
103,Monitor 24 pulg,150.00,8
104,Cable HDMI,5.99,50"""

with open('inventario.csv', 'w', encoding='utf-8') as f:
    f.write(csv_data)
    print("Archivo 'inventario.csv' creado exitosamente.")

# 2. Crear un archivo TXT (notas.txt)
txt_data = """REUNIÓN DE EQUIPO - 01/10
- Revisar presupuesto anual.
- Actualizar licencias de software.
- Comprar café para la oficina.

PENDIENTES:
- Llamar al proveedor de internet."""

with open('notas.txt', 'w', encoding='utf-8') as f:
    f.write(txt_data)
    print("Archivo 'notas.txt' creado exitosamente.")