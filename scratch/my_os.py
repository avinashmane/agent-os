from agno.agent import Agent
from agno.models.google import Gemini 
from agno.os import AgentOS
from agno.db.postgres import PostgresDb
from agno.tools.mcp import MCPTools
from dotenv import load_dotenv
from agno.tools.duckduckgo import DuckDuckGoTools
load_dotenv()
import os

model = Gemini(id=os.environ.get("MODEL", "gemini-2.0-flash-001"))

# Setup the database
db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")


def create_mcp_agent(model):
    # Create MCPTools instance
    mcp_tools = MCPTools(
        transport="streamable-http", 
        url="http://localhost:8123/mcp"
    )

    # Create MCP-enabled agent
    agent = Agent(
        model=model,
        id="agno-agent",
        name="Agno Agent",
        tools=[mcp_tools],
    )
    return agent

agent = create_mcp_agent(model)

# print("MCP Tools initialized.", agent)

assistant = Agent(
    name="Assistant",
    # model=model,
    instructions=["You are a helpful AI assistant."],
    markdown=True,
)

# Create your agents
web_research_agent = Agent(
    name="Web Research Agent",
    model=model,
    db=db,
    tools=[DuckDuckGoTools()],
    markdown=True,
)

agents = [assistant,
            web_research_agent,
            create_mcp_agent(model) # agent,
            ]
     
agent_os = AgentOS(
    os_id="my-first-os",
    description="My first AgentOS",
    agents=agents,
)

app = agent_os.get_app()

if __name__ == "__main__":
    # Default port is 7777; change with port=...
    agent_os.serve(app="my_os:app", reload=True)