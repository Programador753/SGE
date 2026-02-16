import os
import dspy
import ast
from dotenv import load_dotenv
from database import DataManager
from agent import SQLAgentModule

# --- Librerías para UI ---
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

# Inicializar consola
console = Console()

load_dotenv()

def setup_dspy():
    turbo = dspy.LM(
        model='openai/google/gemini-2.5-flash', 
        api_key=os.getenv("OPENROUTER_API_KEY"),
        api_base='https://openrouter.ai/api/v1',
        max_tokens=1024,
        temperature=0
    )
    dspy.configure(lm=turbo)

def print_result_table(result_str):
    """Intenta convertir el string de resultado en una tabla bonita."""
    try:
        # Convertir el string "[('A', 1), ...]" a lista real de Python
        data = ast.literal_eval(result_str)
        
        if isinstance(data, list) and len(data) > 0:
            table = Table(show_header=True, header_style="bold magenta")
            
            # Detectar número de columnas basado en la primera fila
            num_cols = len(data[0]) if isinstance(data[0], (list, tuple)) else 1
            
            # Crear cabeceras genéricas (o inferirlas si el agente devolviera metadatos)
            for i in range(num_cols):
                table.add_column(f"Columna {i+1}")

            # Añadir filas
            for row in data:
                # Asegurarse de que cada elemento sea string para Rich
                if isinstance(row, (list, tuple)):
                    row_str = [str(cell) for cell in row]
                    table.add_row(*row_str)
                else:
                    table.add_row(str(row))
            
            console.print(table)
        else:
            console.print(f"[yellow]El resultado no es una lista o está vacío:[/yellow] {result_str}")
            
    except (ValueError, SyntaxError):
        # Si no puede convertirlo (ej: es un mensaje de error plano), lo imprime normal
        console.print(Panel(str(result_str), title="Respuesta Texto", border_style="blue"))

def main():
    console.rule("[bold blue]Agente SQL Inteligente[/bold blue]")
    
    setup_dspy()
    
    with console.status("[bold green]Conectando e indexando base de datos...", spinner="dots"):
        try:
            manager = DataManager()
            manager.indexar_esquema()
            console.print("[green] Sistema listo.[/green]")
        except Exception as e:
            console.print(f"[bold red]Error inicializando:[/bold red] {e}")
            return

    agent = SQLAgentModule(manager)
    
    console.print("\n[italic grey]Escribe 'salir' para terminar.[/italic grey]\n")

    while True:
        try:
            # Entrada de usuario con estilo
            user_input = console.input("[bold cyan]Pregunta > [/bold cyan]")
            if user_input.lower() in ['salir', 'exit']:
                console.print("[yellow]Cerrando sesión... ¡Adiós![/yellow]")
                break
            
            # Spinner mientras el agente piensa
            sql_response = ""
            with console.status("[bold green]Razonando y buscando tablas...", spinner="aesthetic"):
                sql_response = agent(question=user_input)
            
            # Limpieza
            clean_sql = sql_response.replace("```sql", "").replace("```", "").strip()
            
            # Mostrar SQL con resaltado de sintaxis
            console.print("\n[bold]SQL Generado:[/bold]")
            syntax = Syntax(clean_sql, "sql", theme="monokai", line_numbers=False)
            console.print(syntax)
            console.print("") # Espacio
            
            # Ejecución y Tabla
            with console.status("[bold blue]Ejecutando en base de datos...", spinner="dots"):
                result = manager.execute_sql(clean_sql)
            
            print_result_table(result)
            console.rule() # Línea separadora
            
        except Exception as e:
            console.print(f"[bold red]Error crítico:[/bold red] {e}")

if __name__ == "__main__":
    main()