import dspy

# 1. Configurar el LLM
turbo = dspy.OpenAI(model='gemini-2.5-flash')
dspy.settings.configure(lm=turbo)

# 2. Definir la Signatura (Input -> Output)
class TextToSQL(dspy.Signature):
    """Transforma una pregunta en lenguaje natural a una consulta SQL válida basada en el esquema dado."""
    
    question = dspy.InputField(desc="La pregunta del usuario sobre los datos")
    schema = dspy.InputField(desc="El esquema de las tablas relevantes (CREATE TABLE statements)")
    sql_query = dspy.OutputField(desc="La consulta SQL ejecutable que responde a la pregunta")

# 3. Crear el Módulo (CoT = Chain of Thought para razonamiento)
class SQLGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        # Usamos ChainOfThought para que el modelo razone antes de escribir SQL
        self.generate_sql = dspy.ChainOfThought(TextToSQL)
    
    def forward(self, question, schema):
        return self.generate_sql(question=question, schema=schema)