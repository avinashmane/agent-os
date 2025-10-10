# Create Postgres-backed vector store
from .database import db_url
from agno.vectordb.pgvector import PgVector
from agno.knowledge.embedder.google import GeminiEmbedder

def get_vector_db(table_name="vectors"):
    return PgVector(
        db_url=db_url,
        table_name=table_name,
        embedder=GeminiEmbedder(),
)