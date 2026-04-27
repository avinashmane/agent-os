from agno.db.postgres import PostgresDb
# from agno.models.openai import OpenAIChat
# from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.registry import Registry
from agno.tools.calculator import CalculatorTools
from agno.tools.websearch import WebSearchTools
from agno.vectordb.pgvector import PgVector
from pydantic import BaseModel
from agno import AgentOS, AgentOSConfig

class InputSchema(BaseModel):
    input: str
    description: str

def custom_evaluator(input: str) -> bool:
    return "urgent" in input.lower()

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai", id="postgres_db")

registry = Registry(
    name="My Registry",
    tools=[CalculatorTools(), WebSearchTools()],
    models=["google:gemini-2.0-flash"],
    dbs=[db],
    vector_dbs=[PgVector(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai", table_name="embeddings")],
    schemas=[InputSchema],
    functions=[custom_evaluator],
)

config = AgentOSConfig(
    # List allowed frontend origins here
    allow_origins=["https://your-app.com", "http://localhost:3000"] 
)
agent_os = AgentOS(id="my-app", registry=registry, db=db)
app = agent_os.get_app()