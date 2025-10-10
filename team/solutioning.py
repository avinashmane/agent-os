from agno.agent import Agent
from agno.team import Team
from lib import get_db, get_vector_db, get_model
from agents import create_basic_agents, create_mcp_agent
from agno.tools.user_control_flow import UserControlFlowTools

team_agents = {}
from agents.estimation import chat_agent
team_agents["estimation"] = chat_agent
# Create your agents
team_agents["mcp"] = create_mcp_agent(get_model())

sol_team = Team(
    id="solutioning-team",
    name="Solution Team",
    model=get_model(),
    enable_agentic_state=True,
    tools=[UserControlFlowTools()],
    db=get_db(),
    members=team_agents.values())