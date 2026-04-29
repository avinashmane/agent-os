# Create Postgres-backed vector store
from .database import db_url, get_db
from agno.vectordb.pgvector import PgVector
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.google import GeminiEmbedder

db=None

def get_vector_db(table_name="vectors"):
    db= PgVector(
        db_url=db_url,
        table_name=table_name,
        embedder=GeminiEmbedder(),
    )
    return db

def get_knowledge_base( name="My PG Vector Knowledge Base",
    description="This is a knowledge base that uses a PG Vector DB",
    vector_db=None):

    return Knowledge(
    name=name,
    description=description,
    vector_db=vector_db if vector_db else get_vector_db(),
)