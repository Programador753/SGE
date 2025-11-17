from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# --- 1. Configuración de Selenium ---
driver = webdriver.Firefox()
url = "https://www.xataka.com/espacio/nasa-va-a-recortar-presupuesto-hubble-su-salvacion-pasa-dos-multimillonarios-sector-privado"
driver.get(url)

try:
    # --- 3. Obtener el HTML y cerrar Selenium ---
    # Pedido 1: Extrae su código HTML
    # Obtenemos el código fuente de la página YA RENDERIZADA por el navegador
    html_completo = driver.page_source
    
    print("="*40)
    print("1. CÓDIGO HTML (primeros 500 caracteres)")
    print("="*40)
    print(html_completo)
    print("\n")

    # Cerramos el navegador, ya no lo necesitamos
    driver.quit()

    # --- 4. Análisis con Beautiful Soup ---
    # Creamos un objeto 'soup' para analizar el HTML que obtuvimos
    soup = BeautifulSoup(html_completo, 'html.parser')

    # Pedido 2: Obtén el título de la página <title>
    titulo_pagina = soup.title.string
    print("="*40)
    print("2. TÍTULO DE LA PÁGINA (<title>)")
    print("="*40)
    print(titulo_pagina)
    print("\n")

    # Pedido 3: Obtén todas las etiquetas <li> con la clase específica
    print("="*40)
    print("3. ETIQUETAS <li> DEL MENÚ DE TEMAS")
    print("="*40)
    
    # Buscamos todos los 'li' que tengan exactamente esa clase
    lista_li = soup.find_all('li', class_='masthead-nav-topics-item')
    
    if lista_li:
        for item_li in lista_li:
            # Extraemos el texto limpio de cada 'li'
            print(f"- {item_li.get_text(strip=True)}")
    else:
        print("No se encontraron <li> con esa clase.")
    print("\n")

    # Pedido 4: Extrae el texto de la noticia limpio
    print("="*40)
    print("4. TEXTO LIMPIO DE LA NOTICIA")
    print("="*40)
    
    # Inspeccionando la web, vemos que el contenido está en <div class="article-content">
    # La mejor forma de sacar el texto limpio es buscar los párrafos (<p>)
    # que están dentro de ese contenedor.
    
    contenedor_articulo = soup.find('div', class_='article-content')
    
    if contenedor_articulo:
        # Encontramos todos los párrafos dentro de ese div
        parrafos = contenedor_articulo.find_all('p')
        
        texto_limpio = ""
        for p in parrafos:
            # Añadimos el texto de cada párrafo con un doble salto de línea
            texto_limpio += p.get_text(strip=True) + "\n\n"
        
        print(texto_limpio)
    else:
        print("No se pudo encontrar el contenedor del artículo.")

except Exception as e:
    print(f"Ocurrió un error: {e}")
    driver.quit()