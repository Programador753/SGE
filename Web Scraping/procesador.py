import pandas as pd
import re

def limpiar_texto(texto):
    """
    Limpia el texto eliminando caracteres irrelevantes
    """
    # Convertir a string por si acaso
    texto = str(texto)
    
    # Eliminar caracteres especiales y símbolos, mantener letras, números y espacios
    texto = re.sub(r'[^\w\sáéíóúÁÉÍÓÚñÑüÜ.,!?¿¡]', ' ', texto)
    
    # Eliminar espacios múltiples
    texto = re.sub(r'\s+', ' ', texto)
    
    # Eliminar espacios al inicio y final
    texto = texto.strip()
    
    # Convertir a minúsculas (opcional, puedes comentar esta línea si no quieres)
    texto = texto.lower()
    
    return texto

def convertir_valoracion(rating):
    """
    Convierte valoración de 0-10 a binario:
    - Mayor o igual a 5: 1 (positivo)
    - Menor que 5: 0 (negativo)
    """
    try:
        rating = float(rating)
        return 1 if rating >= 5 else 0
    except:
        return 0

def procesar_reviews(archivo_entrada, archivo_salida):
    """
    Procesa el archivo de reviews y guarda el resultado
    """
    print("Leyendo archivo de reviews...")
    # Leer el CSV
    df = pd.read_csv(archivo_entrada)
    
    print(f"Total de reviews: {len(df)}")
    
    # Limpiar los textos
    print("Limpiando textos...")
    df['texto_procesado'] = df['Review'].apply(limpiar_texto)
    
    # Convertir valoraciones
    print("Convirtiendo valoraciones...")
    df['valoracion'] = df['Rating'].apply(convertir_valoracion)
    
    # Crear el dataframe final con las columnas en el orden correcto
    df_final = df[['valoracion', 'texto_procesado']]
    
    # Guardar en CSV
    print(f"Guardando en {archivo_salida}...")
    df_final.to_csv(archivo_salida, index=False, encoding='utf-8')
    
    # Mostrar estadísticas
    print("\n=== ESTADÍSTICAS ===")
    print(f"Total de reviews procesadas: {len(df_final)}")
    print(f"Reviews positivas (1): {(df_final['valoracion'] == 1).sum()}")
    print(f"Reviews negativas (0): {(df_final['valoracion'] == 0).sum()}")
    print(f"\nArchivo guardado exitosamente en: {archivo_salida}")

if __name__ == "__main__":
    # Archivos de entrada y salida
    archivo_entrada = "reviews.csv"
    archivo_salida = "reviews_procesados.csv"
    
    # Procesar
    procesar_reviews(archivo_entrada, archivo_salida)
    
    print("\n¡Proceso completado!")