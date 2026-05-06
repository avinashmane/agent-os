from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIResponses, OpenAILike
from agno.tools.yfinance import YFinanceTools

from dotenv import load_dotenv
import os
load_dotenv(f"{os.path.dirname(__file__)}/../../.env")

db = SqliteDb(db_file="tmp/agents.db")

agent = Agent(
    model=OpenAILike(id=os.getenv("MODEL","gpt-5.2"),base_url=os.getenv("OPENAI_API_BASE"),api_key=os.getenv("OPENAI_API_KEY")),
    tools=[YFinanceTools()],
    db=db,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

session_id = "finance-session"

print(f"OPENAI_API_BASE:{os.getenv('OPENAI_API_BASE')}, MODEL:{os.getenv('MODEL')} ")

# Turn 1: Analyze a stock
agent.print_response(
    "Give me a quick analysis of NVIDIA",
    session_id=session_id,
    stream=True,
)

# Turn 2: The agent remembers NVDA from turn 1
agent.print_response(
    "Compare that to AMD",
    session_id=session_id,
    stream=True,
)

# Turn 3: Ask based on full conversation
agent.print_response(
    "Which looks like the better investment?",
    session_id=session_id,
    stream=True,
)