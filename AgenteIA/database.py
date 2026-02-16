import os
from langchain_community.utilities import SQLDatabase
from langchain_community.vectorstores import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from qdrant_client import QdrantClient

class DataManager:
    def __init__(self):
        # Inicializa embeddings locales para no depender de APIs externas para vectores
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name="intfloat/multilingual-e5-large",
            model_kwargs={'device': 'cpu'}, # Cambia a 'cuda' si tienes tarjeta gráfica NVIDIA
            encode_kwargs={'normalize_embeddings': True}
        )

        self.db = self._connect_mysql()
        self.vector_store = None
        self.retriever = None

    def _connect_mysql(self):
        """Establece la conexión con MySQL usando SQLAlchemy."""
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT", "3300")
        db_name = os.getenv("DB_NAME")
        
        # Construcción de la cadena de conexión
        uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db_name}"
        print(f"Conectando a MySQL en {host}...")
        return SQLDatabase.from_uri(uri)

    def indexar_esquema(self):
        """Lee el esquema de MySQL y lo indexa en Qdrant Cloud."""
        print("Indexando esquemas en Qdrant Cloud...")
        
        url = os.getenv("QDRANT_URL")
        api_key = os.getenv("QDRANT_API_KEY")
        collection_name = "schema_mysql_prod"

        if not url or not api_key:
            raise ValueError("Faltan credenciales de Qdrant en el archivo .env")

        # Extraer DDL de las tablas
        tablas = self.db.get_usable_table_names()
        docs = []
        for table in tablas:
            ddl = self.db.get_table_info([table])
            docs.append(Document(page_content=ddl, metadata={"table_name": table}))

        # Cargar en Qdrant
        # force_recreate=True asegura que el esquema esté siempre actualizado al iniciar
        self.vector_store = Qdrant.from_documents(
            docs,
            self.embeddings,
            url=url,
            api_key=api_key,
            collection_name=collection_name,
            force_recreate=True
        )
        
        # Configurar el recuperador (Top 5 tablas más relevantes)
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})
        print("Indexación completada.")

    def get_relevant_tables(self, query):
        """Recupera los esquemas de tablas relevantes para la pregunta."""
        if not self.retriever:
            raise RuntimeError("El esquema no ha sido indexado. Ejecuta indexar_esquema() primero.")
        return self.retriever.invoke(query)

    def execute_sql(self, query):
        """Ejecuta la consulta SQL en la base de datos."""
        return self.db.run(query)