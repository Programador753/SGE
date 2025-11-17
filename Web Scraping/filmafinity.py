"""
Traducción a Python del script de scraping de FilmAffinity.

Este script obtiene las películas mejor valoradas, guarda su información en 'movies.csv',
y luego extrae todas las reseñas de cada película, guardándolas en 'reviews.csv'.

MODIFICADO para usar Selenium y evitar la detección de bots.

CONFIGURACIÓN:
- num_clicks en get_top_films(): Controla cuántas veces hace clic en "Ver más" para cargar películas
  * 0 clics = ~31 películas (solo carga inicial)
  * 3 clics = ~60-80 películas
  * 5 clics = ~90-120 películas (por defecto)
  * 10 clics = ~150-200 películas
  * 15+ clics = Todas las películas del Top (hasta que no haya más)
  * Ajusta según cuántas reseñas necesites (cada película tiene ~50-100 páginas de reseñas)

TIEMPOS DE ESPERA ANTI-BOT:
- 2-3 segundos: Después de cargar cada página de reseñas (simula lectura)
- 5-9 segundos: Entre páginas de reseñas de la misma película
- 4-6 segundos: Al detectar número de páginas (espera JavaScript)
- 8-12 segundos: Entre películas completas
- 4-6 segundos: Después de cada clic en "Ver más" (para cargar más películas del Top)
- 1-2 segundos: Entre películas al escanear el Top
Estos tiempos aleatorios simulan comportamiento humano y evitan bloqueos.
"""

import csv
import sys
import time
import random
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

# Imports de Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# --- Estructuras de Datos ---

@dataclass
class Movie:
    """Almacena información sobre una película."""
    id: int
    title: str
    year: int
    image: str
    pages: int

@dataclass
class Rating:
    """Almacena la información de una reseña."""
    rating: Optional[int]
    review: Optional[str]

# --- Constantes ---

URL_PREFIX = "https://www.filmaffinity.com/es/reviews/"

# --- Cabecera de User-Agent (Selenium la usará) ---
# Usamos el mismo User-Agent para consistencia
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"


# --- Funciones de Scraping (Modificadas para Selenium) ---

def scrap_review_page(driver: webdriver.Chrome, movie_id: int, page: int, csv_writer: csv.writer) -> None:
    """
    Extrae las reseñas de una página específica para una película y las escribe en un CSV.
    Usa el driver de Selenium para obtener la página.
    """
    url = f"{URL_PREFIX}{page}/{movie_id}.html"
    print(f"  - Scraping página de reseña: {url}")
    
    try:
        driver.get(url)
        
        # ESPERA EXPLÍCITA: Esperar hasta que aparezca el contenedor de reseñas
        wait = WebDriverWait(driver, 25)  # Espera máximo 25 segundos
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.reviews-cards-wrapper")))
        
        # Espera adicional a que se carguen las reseñas individuales
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.review-wrapper.rw-item")))
        
        # Espera aleatoria adicional para simular lectura humana (2-3 segundos)
        read_time = random.uniform(2.0, 3.0)
        time.sleep(read_time)
        
        print(f"  - Página cargada, extrayendo contenido...")
        
    except TimeoutException:
        print(f"  - Timeout esperando reseñas en página {page}. Saltando...", file=sys.stderr)
        return
    except Exception as e:
        print(f"  - Error al cargar la página: {str(e)[:100]}. Saltando...", file=sys.stderr)
        return

    data = driver.page_source
    soup = BeautifulSoup(data, 'lxml')
    
    # Selector confirmado del HTML real
    html_reviews = soup.select("div.review-wrapper.rw-item")
    
    if not html_reviews:
        print(f"  - No se encontraron reseñas en la página {page} para la película {movie_id}.")
        return

    print(f"  - Encontradas {len(html_reviews)} reseñas en la página {page}")
    ratings: List[Rating] = []

    for idx, review_element in enumerate(html_reviews):
        rating_text: Optional[str] = None
        review_text: Optional[str] = None
        
        # Selector confirmado: div.fa-user-rat-box
        rating_elem = review_element.select_one("div.fa-user-rat-box")
        if rating_elem:
            rating_text = rating_elem.get_text(strip=True)
            
        # Selector confirmado: div.rev-text1
        review_elem = review_element.select_one("div.rev-text1")
        if review_elem:
            # Extraer solo el texto dentro de los divs con clase mx-3
            text_divs = review_elem.select("div.mx-3")
            if text_divs:
                # Unir el texto de todos los divs
                review_text = " ".join([div.get_text(strip=True) for div in text_divs])
            else:
                review_text = review_elem.get_text(strip=True)
            
        # Intenta convertir la puntuación a entero
        rating_val: Optional[int] = None
        if rating_text:
            try:
                rating_val = int(rating_text)
            except ValueError:
                rating_val = None
        
        ratings.append(Rating(rating=rating_val, review=review_text))

    # Escribir las reseñas en el archivo CSV
    for rating in ratings:
        review_str = rating.review or ""
        rating_str = str(rating.rating) if rating.rating is not None else ""
        csv_writer.writerow([review_str, rating_str])
    
    print(f"  - Guardadas {len(ratings)} reseñas en el CSV")
    
    # Espera aleatoria entre páginas para evitar detección de bot (5-9 segundos)
    wait_time = random.uniform(5.0, 9.0)
    print(f"  - Esperando {wait_time:.1f}s antes de la siguiente página...")
    time.sleep(wait_time)

def scrap_film(driver: webdriver.Chrome, movie_id: int, pages: int, csv_writer: csv.writer) -> None:
    """
    Extrae todas las páginas de reseñas de una película.
    Pasa el driver de Selenium a la función de scraping de página.
    """
    if pages > 0:
        print(f"Scraping {pages} página(s) para la película ID: {movie_id}")
        for i in range(1, pages + 1):
            scrap_review_page(driver, movie_id, i, csv_writer)
        
        # Espera más larga entre películas para evitar detección (8-12 segundos)
        wait_time = random.uniform(8.0, 12.0)
        print(f"Película completada. Esperando {wait_time:.1f}s antes de la siguiente película...")
        time.sleep(wait_time)
    else:
        print(f"No hay páginas para scrapear de la película ID: {movie_id}")


def get_pages(driver: webdriver.Chrome, movie_id: int) -> int:
    """
    Obtiene el número total de páginas de reseñas para una película.
    Usa el driver de Selenium.
    """
    url = f"{URL_PREFIX}1/{movie_id}.html"
    print(f"Obteniendo número de páginas para ID: {movie_id} desde {url}")
    
    try:
        driver.get(url)
        
        # Esperar a que el body esté presente primero
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Espera aleatoria para simular comportamiento humano (4-6 segundos)
        wait_time = random.uniform(4.0, 6.0)
        print(f"  - Esperando {wait_time:.1f}s para que JavaScript cargue completamente...")
        time.sleep(wait_time)
        
        # Intentar esperar al contenedor de reseñas (pero no fallar si no aparece)
        try:
            wait_short = WebDriverWait(driver, 5)
            wait_short.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.reviews-cards-wrapper")))
            print("  - Contenedor de reseñas encontrado")
        except TimeoutException:
            print("  - Contenedor de reseñas no encontrado rápidamente, continuando...")
        
    except TimeoutException:
        print(f"  - Timeout esperando que cargue la página. Asumiendo 1 página.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"  - Error cargando página: {str(e)[:100]}. Asumiendo 1 página.", file=sys.stderr)
        return 1

    data = driver.page_source
    soup = BeautifulSoup(data, 'lxml')
    
    # Intentar múltiples selectores para el paginador
    page_links = []
    
    # Selector 1: Bootstrap completo
    page_links = soup.select("ul.pagination li.page-item a.page-link")
    print(f"  - DEBUG: Enlaces con 'ul.pagination li.page-item a.page-link': {len(page_links)}")
    
    # Selector 2: Solo pagination
    if not page_links:
        page_links = soup.select("ul.pagination a")
        print(f"  - DEBUG: Enlaces con 'ul.pagination a': {len(page_links)}")
    
    # Selector 3: Cualquier paginador
    if not page_links:
        page_links = soup.select(".pagination a")
        print(f"  - DEBUG: Enlaces con '.pagination a': {len(page_links)}")
    
    # Selector 4: Enlaces en div con clase pager
    if not page_links:
        page_links = soup.select("div.pager a, nav.pager-bs a")
        print(f"  - DEBUG: Enlaces con 'div.pager a' o 'nav.pager-bs a': {len(page_links)}")
    
    if page_links:
        # Extraer solo los textos que son números
        page_numbers = []
        for link in page_links:
            text = link.get_text(strip=True)
            try:
                page_num = int(text)
                page_numbers.append(page_num)
            except ValueError:
                continue
        
        print(f"  - DEBUG: Números de página encontrados: {page_numbers}")
        
        if page_numbers:
            max_pages = max(page_numbers)
            print(f"  - Encontradas {max_pages} páginas.")
            return max_pages
    
    # Si no hay paginador, verificar si hay al menos una reseña
    reviews = soup.select("div.review-wrapper.rw-item, div.review-wrapper")
    print(f"  - DEBUG: Reseñas encontradas: {len(reviews)}")
    
    if reviews:
        print("  - No se encontró paginador pero hay reseñas. Asumiendo 1 página.")
        return 1
    
    print("  - ADVERTENCIA: No se encontró paginador ni reseñas.")
    # Guardar HTML para debug
    debug_file = f"debug_get_pages_{movie_id}.html"
    try:
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(data)
        print(f"  - HTML guardado en '{debug_file}' para inspección")
    except:
        pass
    
    return 1


def get_top_films(driver: webdriver.Chrome, num_clicks: int = 5, debug: bool = False) -> List[Movie]:
    """
    Extrae las películas del Top de FilmAffinity haciendo clic en "Ver más resultados".
    Usa el driver de Selenium.
    
    Args:
        driver: Driver de Selenium
        num_clicks: Número de veces que hará clic en el botón para cargar más películas (default: 5)
        debug: Si es True, guarda el HTML después de cada clic (default: False)
    """
    url = "https://www.filmaffinity.com/es/topgen.php?orderby=raa"
    print(f"\n=== Obteniendo películas del Top desde: {url} ===")
    print(f"Se hará clic {num_clicks} veces en 'Ver más resultados' para cargar más películas")
    if debug:
        print("MODO DEBUG ACTIVADO: Se guardará el HTML después de cada clic")
    
    try:
        driver.get(url)
        # Espera inicial para cargar la página
        wait_time = random.uniform(3.0, 5.0)
        print(f"  - Esperando {wait_time:.1f}s para que cargue la página inicial...")
        time.sleep(wait_time)
    except WebDriverException as e:
        print(f"Error al obtener el Top: {e}", file=sys.stderr)
        return []
    
    # Hacer clic en el botón "Ver más" para cargar más películas
    for click_num in range(1, num_clicks + 1):
        print(f"\n  - Clic {click_num}/{num_clicks}: Intentando hacer clic en 'Ver más resultados'...")
        
        try:
            # Esperar explícitamente a que el botón esté presente y sea clickable
            wait = WebDriverWait(driver, 10)
            load_more_button = wait.until(
                EC.presence_of_element_located((By.ID, "load-more-bt"))
            )
            
            # Verificar si el botón es visible
            if not load_more_button.is_displayed():
                print(f"    [X] El boton 'Ver mas' no esta visible. Posiblemente no hay mas peliculas.")
                break
            
            # Hacer scroll hasta el botón para asegurar que sea visible
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", load_more_button)
            time.sleep(1.5)
            
            # Contar películas antes del clic
            movies_before = len(driver.find_elements(By.CSS_SELECTOR, "div.movie-card.mc-flex.movie-card-0"))
            print(f"    Películas antes del clic: {movies_before}")
            
            # Intentar hacer clic de múltiples formas
            click_success = False
            
            # Método 1: Clic normal
            try:
                load_more_button.click()
                print(f"    [OK] Clic normal realizado")
                click_success = True
            except Exception as e1:
                print(f"    [!] Clic normal fallo: {str(e1)[:50]}")
                
                # Método 2: Clic con JavaScript
                try:
                    driver.execute_script("arguments[0].click();", load_more_button)
                    print(f"    [OK] Clic con JavaScript realizado")
                    click_success = True
                except Exception as e2:
                    print(f"    [!] Clic con JavaScript fallo: {str(e2)[:50]}")
                    
                    # Método 3: Clic con ActionChains
                    try:
                        from selenium.webdriver.common.action_chains import ActionChains
                        actions = ActionChains(driver)
                        actions.move_to_element(load_more_button).click().perform()
                        print(f"    [OK] Clic con ActionChains realizado")
                        click_success = True
                    except Exception as e3:
                        print(f"    [X] Todos los metodos de clic fallaron")
                        break
            
            if click_success:
                print(f"    Esperando a que se carguen más películas vía AJAX...")
                
                # MÉTODO 1: Esperar a que aparezca el indicador de carga y desaparezca
                try:
                    # Esperar a que el indicador de carga aparezca (máx 5 segundos)
                    loading_wait = WebDriverWait(driver, 5)
                    loading_indicator = loading_wait.until(
                        EC.visibility_of_element_located((By.ID, "loading"))
                    )
                    print(f"    [~] Indicador de carga detectado...")
                    
                    # Ahora esperar a que desaparezca (máx 20 segundos)
                    disappear_wait = WebDriverWait(driver, 20)
                    disappear_wait.until(
                        EC.invisibility_of_element_located((By.ID, "loading"))
                    )
                    print(f"    [OK] Carga AJAX completada")
                    
                except TimeoutException:
                    print(f"    [!] No se detecto el indicador de carga, intentando metodo alternativo...")
                    
                    # MÉTODO 2: Esperar a que el botón vuelva a ser visible
                    try:
                        button_wait = WebDriverWait(driver, 15)
                        button_wait.until(
                            EC.visibility_of_element_located((By.ID, "load-more-bt"))
                        )
                        print(f"    [OK] Boton 'Ver mas' visible de nuevo")
                    except TimeoutException:
                        print(f"    [!] Boton no volvio a ser visible")
                
                # Espera adicional para asegurar que el DOM se actualizó
                time.sleep(2)
                
                # Hacer scroll para ver las nuevas películas
                driver.execute_script("window.scrollBy(0, 800);")
                time.sleep(1)
                
                # Verificar cuántas películas tenemos ahora
                movies_after = len(driver.find_elements(By.CSS_SELECTOR, "div.movie-card.mc-flex.movie-card-0"))
                new_movies = movies_after - movies_before
                
                if new_movies > 0:
                    print(f"    [OK] Peliculas cargadas: {movies_after} (nuevas: {new_movies})")
                else:
                    print(f"    [!] No se detectaron nuevas peliculas")
                    print(f"    Películas antes: {movies_before}, después: {movies_after}")
                    
                    # Intentar con selector alternativo
                    alt_selector = "li.movie-card-0, div.movie-card"
                    movies_alt = len(driver.find_elements(By.CSS_SELECTOR, alt_selector))
                    print(f"    Intentando selector alternativo '{alt_selector}': {movies_alt} películas")
                    
                    if movies_after == movies_before:
                        print(f"    [i] No se cargaron peliculas nuevas. Probablemente no hay mas.")
                        break
                
                # Espera adicional para que se estabilice
                time.sleep(random.uniform(2.0, 3.0))
                
                # Guardar HTML para depuración si está activado
                if debug:
                    try:
                        debug_file = f"debug_click_{click_num}.html"
                        with open(debug_file, 'w', encoding='utf-8') as f:
                            f.write(driver.page_source)
                        print(f"    [FILE] HTML guardado en '{debug_file}'")
                    except Exception as e:
                        print(f"    [!] No se pudo guardar HTML: {e}")
            else:
                break
                
        except TimeoutException:
            print(f"    [X] Timeout esperando el boton 'Ver mas'. No hay mas peliculas.")
            break
        except Exception as e:
            print(f"    [X] Error: {str(e)[:100]}")
            print(f"    Probablemente se han cargado todas las películas disponibles.")
            break
    
    # Obtener el HTML final después de todos los scrolls
    data = driver.page_source
    soup = BeautifulSoup(data, 'lxml')
    
    # Intentar múltiples selectores para encontrar las películas
    movies_html = soup.select("div.movie-card.mc-flex.movie-card-0")
    print(f"  - Selector 1 'div.movie-card.mc-flex.movie-card-0': {len(movies_html)} películas")
    
    if not movies_html:
        movies_html = soup.select("div.movie-card.mc-flex")
        print(f"  - Selector 2 'div.movie-card.mc-flex': {len(movies_html)} películas")
    
    if not movies_html:
        movies_html = soup.select("div.movie-card")
        print(f"  - Selector 3 'div.movie-card': {len(movies_html)} películas")
    
    if not movies_html:
        # Guardar HTML para inspección
        try:
            with open("debug_final_no_movies.html", 'w', encoding='utf-8') as f:
                f.write(data)
            print(f"  - No se encontraron películas. HTML guardado en 'debug_final_no_movies.html'")
        except:
            pass
        print(f"  - No se encontraron películas. Abortando...")
        return []
    
    print(f"\n  - Total de películas encontradas después de los scrolls: {len(movies_html)}")
    
    movies: List[Movie] = []

    for idx, element in enumerate(movies_html, 1):
        try:
            movie_id_str = element.get('data-movie-id')
            if not movie_id_str:
                continue
                
            movie_id = int(movie_id_str)
            
            title_elem = element.select_one("div.mc-title a")
            title = title_elem.get_text(strip=True) if title_elem else "Título Desconocido"
            
            year_elem = element.select_one("span.mc-year")
            year_str = year_elem.get_text(strip=True) if year_elem else "0"
            year = int(year_str)
            
            image_elem = element.select_one("div.mc-poster img")
            image = image_elem.get('src', '') if image_elem else ""
            
            # Obtener el número de páginas de reseñas para esta película
            # Pasamos el driver a get_pages
            print(f"\n  [{idx}/{len(movies_html)}] Procesando película: {title} (ID: {movie_id})")
            pages = get_pages(driver, movie_id)
            
            movie = Movie(id=movie_id, title=title, year=year, image=image, pages=pages)
            movies.append(movie)
            
            print(f"  [OK] Pelicula añadida: ID: {movie.id}, Titulo: {movie.title}, Año: {movie.year}, Paginas: {movie.pages}")
            
            # Pequeña espera entre películas al escanear el Top (1-2 segundos)
            wait_time = random.uniform(1.0, 2.0)
            time.sleep(wait_time)

        except (AttributeError, ValueError, TypeError) as e:
            print(f"  [X] Error al parsear una pelicula: {e}", file=sys.stderr)
            continue
            
    return movies

# --- Función Principal ---

def main():
    """
    Función principal de ejecución del script.
    """
    movies_csv_path = Path("movies.csv")
    reviews_csv_path = Path("reviews.csv")
    last_review_path = Path("last_review.txt")
    
    movies: List[Movie] = []

    # --- Configuración de Selenium ---
    print("Configurando el driver de Selenium (esto puede tardar la primera vez)...")
    chrome_options = Options()
    
    # CAMBIO: Desactivar headless temporalmente para debug de AJAX
    # Si las películas se cargan correctamente sin headless, el problema es el modo headless
    # chrome_options.add_argument("--headless=new")  # Modo headless DESACTIVADO temporalmente
    
    # Opciones para estabilidad
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(f"user-agent={USER_AGENT}")
    
    # Deshabilitar logging excesivo
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Preferencias adicionales (deshabilitar imágenes para más velocidad)
    # NOTA: Comentado temporalmente - puede interferir con la carga de contenido AJAX
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # chrome_options.add_experimental_option("prefs", prefs)

    # Usar webdriver_manager para instalar y obtener la ruta del driver automáticamente
    try:
        driver_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=driver_service, options=chrome_options)
        driver.set_page_load_timeout(30)  # Timeout de 30 segundos
    except Exception as e:
        print(f"Error fatal al inicializar Selenium/WebDriver: {e}", file=sys.stderr)
        print("Asegúrate de tener Google Chrome instalado.", file=sys.stderr)
        sys.exit(1)
        
    print("Driver de Selenium configurado y listo.")

    try:
        # 1. Cargar o descargar la lista de películas
        if not movies_csv_path.exists():
            print(f"'{movies_csv_path}' no encontrado. Descargando lista de películas...")
            # Pasamos el driver a get_top_films
            # Hacer 15 clics en "Ver más" para obtener muchas más películas
            movies = get_top_films(driver, num_clicks=5)
            
            # Guardar en CSV
            try:
                with movies_csv_path.open('w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID", "Title", "Year", "Image", "Pages"])
                    for movie in movies:
                        writer.writerow([movie.id, movie.title, movie.year, movie.image, movie.pages])
                print(f"Lista de películas guardada en '{movies_csv_path}'")
            except IOError as e:
                print(f"Error al escribir '{movies_csv_path}': {e}", file=sys.stderr)
                sys.exit(1)
                
        else:
            print(f"Cargando lista de películas desde '{movies_csv_path}'...")
            try:
                with movies_csv_path.open('r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)  # Omitir cabecera
                    for row in reader:
                        try:
                            movies.append(Movie(
                                id=int(row[0]),
                                title=row[1],
                                year=int(row[2]),
                                image=row[3],
                                pages=int(row[4])
                            ))
                        except (ValueError, IndexError) as e:
                            print(f"Error al leer fila de movie: {row}, Error: {e}", file=sys.stderr)
                print(f"Cargadas {len(movies)} películas.")
            except IOError as e:
                print(f"Error al leer '{movies_csv_path}': {e}", file=sys.stderr)
                sys.exit(1)
            except StopIteration:
                print(f"'{movies_csv_path}' está vacío o solo tiene cabecera. Saliendo.", file=sys.stderr)
                sys.exit(1)

        # 2. Comprobar si debemos reanudar desde un punto anterior
        all_movies = movies.copy()  # Guardar copia completa de todas las películas
        need_more_movies = False
        if last_review_path.exists():
            try:
                last_reviewed_id = int(last_review_path.read_text(encoding='utf-8').strip())
                print(f"Archivo de reanudación encontrado. Buscando ID: {last_reviewed_id}")
                
                # Encontrar la posición de la última película procesada
                start_index = -1
                for i, movie in enumerate(movies):
                    if movie.id == last_reviewed_id:
                        start_index = i
                        break
                
                if start_index != -1 and start_index + 1 < len(movies):
                    # Reanudar desde la *siguiente* película
                    movies_to_process = movies[start_index + 1:]
                    print(f"Reanudando desde la película '{movies_to_process[0].title}' (ID: {movies_to_process[0].id}). {len(movies_to_process)} películas restantes.")
                    movies = movies_to_process
                elif start_index + 1 >= len(movies):
                    print("Ya se habían procesado todas las películas de la lista actual.")
                    print("Buscando más películas del Top...")
                    need_more_movies = True
                else:
                    print(f"El ID {last_reviewed_id} no se encontró en la lista. Procesando todo.", file=sys.stderr)
                    
            except (IOError, ValueError) as e:
                print(f"Error al leer '{last_review_path}': {e}. Procesando todo.", file=sys.stderr)

        # 3. Si necesitamos más películas, buscarlas y agregarlas
        if need_more_movies:
            print("\n=== Buscando películas adicionales del Top ===")
            existing_ids = {movie.id for movie in all_movies}
            new_movies = get_top_films(driver, num_clicks=5)
            
            # Filtrar solo películas que NO están en la lista actual
            added_count = 0
            movies_to_add = []
            for new_movie in new_movies:
                if new_movie.id not in existing_ids:
                    all_movies.append(new_movie)
                    movies_to_add.append(new_movie)
                    added_count += 1
            
            print(f"Se agregaron {added_count} películas nuevas a la lista.")
            
            # Actualizar el CSV con todas las películas (viejas + nuevas)
            if added_count > 0:
                try:
                    with movies_csv_path.open('w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(["ID", "Title", "Year", "Image", "Pages"])
                        for movie in all_movies:
                            writer.writerow([movie.id, movie.title, movie.year, movie.image, movie.pages])
                    print(f"Lista de películas actualizada en '{movies_csv_path}' (Total: {len(all_movies)} películas)")
                    
                    # Procesar las nuevas películas
                    movies = movies_to_add
                    print(f"Listas para procesar {len(movies)} películas nuevas.")
                except IOError as e:
                    print(f"Error al actualizar '{movies_csv_path}': {e}", file=sys.stderr)
            else:
                print("No se encontraron películas nuevas. Saliendo.")
                movies = []

        if not movies:
            print("No hay películas para procesar. Saliendo.")
            return

        # 4. Abrir el archivo de reseñas en modo 'append' (añadir)
        try:
            # Comprobar si el archivo existe para decidir si escribir la cabecera
            write_header = not reviews_csv_path.exists() or reviews_csv_path.stat().st_size == 0
            
            with reviews_csv_path.open('a', newline='', encoding='utf-8') as f:
                reviews_writer = csv.writer(f)
                
                if write_header:
                    print(f"Creando '{reviews_csv_path}' y escribiendo cabecera.")
                    reviews_writer.writerow(["Review", "Rating"])
                else:
                     print(f"Añadiendo reseñas a '{reviews_csv_path}' existente.")
                
                # 5. Procesar cada película
                for movie in movies:
                    print(f"\n--- Procesando película: {movie.title} (ID: {movie.id}) ---")
                    # Pasamos el driver a scrap_film
                    scrap_film(driver, movie.id, movie.pages, reviews_writer)
                    
                    # Opcional: Actualizar el archivo 'last_review.txt' para reanudar si se interrumpe
                    try:
                        last_review_path.write_text(str(movie.id), encoding='utf-8')
                        print(f"Progreso guardado. Último ID procesado: {movie.id}")
                    except IOError as e:
                        print(f"No se pudo actualizar '{last_review_path}': {e}", file=sys.stderr)
                        
            print("\n--- Proceso de scraping completado. ---")

        except IOError as e:
            print(f"Error al abrir o escribir en '{reviews_csv_path}': {e}", file=sys.stderr)
            sys.exit(1)

    finally:
        # --- MUY IMPORTANTE: Cerrar el driver ---
        # Esto cierra el navegador, incluso si el script falla.
        print("Cerrando el driver de Selenium.")
        driver.quit()


if __name__ == "__main__":
    main()