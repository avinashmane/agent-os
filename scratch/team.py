from agno.team import Team
from agno.models.google import Gemini
from agno.agent import Agent
from dotenv import load_dotenv
load_dotenv()
import os

model = Gemini(id=os.environ.get("MODEL", "gemini-2.0-flash-001"))

agent_1 = Agent(model=model,name="News Agent", role="Get the latest news")

agent_2 = Agent(model=model,name="Weather Agent", role="Get the weather for the next 7 days")

team = Team(model=model,name="News and Weather Team", members=[agent_1, agent_2])

# Synchronous execution
# result = team.run("What is the weather in Tokyo?")

# print(result)
team.print_response("What is the weather in Tokyo?")
# Asynchronous execution
# result = await team.arun("What is the weather in Tokyo?")