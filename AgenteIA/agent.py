import os
import dspy
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ==============================================================================
# 1. CONFIGURACIÓN DEL LLM 
# ==============================================================================
# Usamos dspy.OpenAI porque OpenRouter es compatible con esa librería.
turbo = dspy.LM(
    # "openai/" indica el protocolo, "google/..." es el modelo en OpenRouter
    model='openai/google/gemini-2.5-flash', 
    api_key=os.getenv("OPENROUTER_API_KEY"),
    api_base='https://openrouter.ai/api/v1',
    max_tokens=1024,
    temperature=0
)
dspy.configure(lm=turbo)

# ==============================================================================
# 2. DEFINICIÓN DE FIRMAS (Tus Signatures)
# ==============================================================================

# --- Paso 1: Descubrir tablas (Tu primera "Flor" en la pizarra) ---
class DiscoverTables(dspy.Signature):
    """
    Analiza la pregunta y los esquemas disponibles.
    Selecciona las tablas estrictamente necesarias.
    Devuelve una lista JSON.
    """
    question = dspy.InputField(desc="La pregunta del usuario")
    context = dspy.InputField(desc="Esquemas DDL recuperados (RAG)")
    selected_tables = dspy.OutputField(desc="Lista JSON de tablas. Ej: ['tabla_a', 'tabla_b']")

# --- Paso 2: Generar SQL (Tu código propuesto) ---
class TextToSQL(dspy.Signature):
    """
    Transforma una pregunta en lenguaje natural a una consulta SQL válida 
    basada en el esquema dado. No uses Markdown.
    """
    question = dspy.InputField(desc="La pregunta del usuario sobre los datos")
    database_schema = dspy.InputField(desc="El esquema de las tablas relevantes (CREATE TABLE statements)")
    sql_query = dspy.OutputField(desc="La consulta SQL ejecutable que responde a la pregunta")

# ==============================================================================
# 3. MÓDULO (Lógica del Agente)
# ==============================================================================

class SQLAgentModule(dspy.Module):
    def __init__(self, data_manager):
        super().__init__()
        self.dm = data_manager
        
        # Usamos ChainOfThought para razonamiento en ambos pasos
        self.discover_step = dspy.ChainOfThought(DiscoverTables)
        
        # Aquí está tu generador integrado
        self.generate_sql = dspy.ChainOfThought(TextToSQL)

    def forward(self, question):
        # 1. RAG: Buscar tablas candidatas en Qdrant (o FAISS)
        # Esto trae "posibles" tablas
        raw_docs = self.dm.get_relevant_tables(question)
        context_str = "\n\n".join([d.page_content for d in raw_docs])
        
        # 2. DISCOVER: Filtrar tablas exactas
        print("Analizando tablas necesarias...")
        p1 = self.discover_step(question=question, context=context_str)
        
        # Procesamiento del JSON de tablas
        try:
            clean_json = p1.selected_tables.replace("'", '"')
            table_names = json.loads(clean_json)
            if isinstance(table_names, str): table_names = [table_names]
        except:
            # Fallback si falla el JSON
            table_names = [d.metadata['table_name'] for d in raw_docs[:2]]
        
        print(f"Tablas seleccionadas: {table_names}")

        # 3. GENERATE: Tu lógica TextToSQL
        # Obtenemos el esquema limpio solo de las tablas seleccionadas
        final_schema = self.dm.db.get_table_info(table_names)
        
        # Llamamos a tu módulo
        p2 = self.generate_sql(question=question, database_schema=final_schema)
        
        return p2.sql_query