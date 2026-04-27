from agno.agent.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.os import AgentOS
from agno.os.interfaces.a2a import A2A
from agno.tools.yfinance import YFinanceTools

from dotenv import load_dotenv
load_dotenv()
import os
# os.environ
# from lib import get_db, get_vector_db, get_model

agent = Agent(
    name="my-agent",
    model="google:gemini-2.0-flash",#OpenAIResponses(id="gpt-5.2"),
    tools=[
        YFinanceTools(),#stock_price=True, analyst_recommendations=True, company_info=True),
    ],
    description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals.",
    instructions="Format your response using markdown and use tables to display data where possible.",
)

agent_os = AgentOS(
    agents=[agent],
    a2a_interface=True,
)
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="a2a_agent_with_tools:app", reload=True)