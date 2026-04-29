import asyncio

from agno.agent import Agent
from agno.db.postgres.postgres import PostgresDb
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector
from agno.knowledge.embedder.google import GeminiEmbedder
from dotenv import load_dotenv
load_dotenv()
import os
from agno.models.google import Gemini

db = PostgresDb(
    db_url=os.getenv("DB_URL"),
    knowledge_table="knowledge_contents",
)

# Create Knowledge Instance
knowledge = Knowledge(
    name="Basic SDK Knowledge Base",
    description="Agno 2.0 Knowledge Implementation",
    contents_db=db,
    vector_db=PgVector(
        table_name="vectors", db_url=os.getenv("DB_URL"),
        embedder=GeminiEmbedder()
        
    ),
)
# Add from URL to the knowledge base
asyncio.run(
    knowledge.add_content_async(
        name="Recipes",
        url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
        metadata={"user_tag": "Recipes from website"},
    )
)

agent = Agent(
    model=Gemini(id=os.environ.get("MODEL", "gemini-2.0-flash-001")),
    name="My Agent",
    description="Agno 2.0 Agent Implementation",
    knowledge=knowledge,
    search_knowledge=True,
    debug_mode=True,
)

agent.print_response(
    "How do I make chicken and galangal in coconut milk soup?",
    markdown=True,
)