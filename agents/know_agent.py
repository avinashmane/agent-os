from agno.knowledge.knowledge import Knowledge
from agno.db.postgres import PostgresDb
from agno.vectordb.pgvector import PgVector
from agno.agent import Agent

from lib import get_db, model, get_vector_db
from box import Box

cfg=Box.from_yaml("""
knowledge_table: knowledge_table
vector_table: vectors                  
""")

# Setup the database
db_url="postgresql+psycopg://ai:ai@localhost:5532/ai"

# ContentsDB is required for AgentOS Knowledge page
contents_db = get_db(
    knowledge_table=cfg.knowledge_table
)

vector_db = get_vector_db(table_name=cfg.vector_table)


knowledge = Knowledge(
    vector_db=vector_db,
    contents_db=contents_db  # Must be provided for AgentOS
)

rag_agent = Agent(
    model=model,
    name="Knowledge Agent",
    knowledge=knowledge
)