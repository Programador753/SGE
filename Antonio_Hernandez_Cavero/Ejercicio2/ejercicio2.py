# Definición de las clases Data_Breast y Tripleta
class Data_Breast:
    def __init__(self, id_hospital, diagnosis, radius_mean): 
        self.id_hospital = id_hospital  
        self.diagnosis = diagnosis 
        self.radius_mean = radius_mean 

# Definición de la clase Tripleta 
class Tripleta:
    def __init__(self, id_hospital, min_radius, max_radius):
        self.id_hospital = id_hospital
        self.min_radius = min_radius
        self.max_radius = max_radius

# Proceso archivo CSV para sacar los datos necesarios
with open('Breast_Cancer_Data_Final.csv', 'r') as file:
    lines = file.readlines()

data_breast_list = [] # Lista para almacenar objetos Data_Breast
for line in lines[1:]:  # Saltar la cabecera
    parts = line.strip().split(',') # Dividir por comas
    id_hospital = int(parts[32]) # ID del hospital 
    diagnosis = parts[1] # Diagnóstico (M o B)
    radius_mean = float(parts[2]) # Media de las distancias desde el centro a los puntos del perímetro

    # Crear objeto Data_Breast y añadirlo a la lista
    data_breast = Data_Breast(id_hospital, diagnosis, radius_mean)
    data_breast_list.append(data_breast)


# Implementación del método min_max_radius_mean
def min_max_radius_mean(data_breast_list):
    hospital_data = {}

    # Recorremos la lista de datos
    for data in data_breast_list:
        if data.diagnosis == 'M':
            if data.id_hospital not in hospital_data:
                # Inicializar min y max con el primer valor encontrado
                hospital_data[data.id_hospital] = {
                    'min': data.radius_mean, 
                    'max': data.radius_mean
                }
            else:
                if data.radius_mean < hospital_data[data.id_hospital]['min']:
                    hospital_data[data.id_hospital]['min'] = data.radius_mean
                if data.radius_mean > hospital_data[data.id_hospital]['max']:
                    hospital_data[data.id_hospital]['max'] = data.radius_mean

    result = [] # Lista para almacenar las tripletas

    # Crear las tripletas a partir de los datos recopilados
    for id_hospital, values in hospital_data.items():
        triplet = Tripleta(id_hospital, values['min'], values['max'])
        result.append(triplet)

    return result

# Llamada al método y muestra de resultados
tripletas = min_max_radius_mean(data_breast_list)
for tripleta in tripletas:
    print(f"Hospital ID: {tripleta.id_hospital} | Min Radius Mean: {tripleta.min_radius} | Max Radius Mean: {tripleta.max_radius}")

