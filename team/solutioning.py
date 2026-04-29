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
    session_state="sol_state",
    add_session_state_to_context=True,
    tools=[],#UserControlFlowTools()
    db=get_db(),
    members=list(team_agents.values()),
    debug_mode = True,
    add_history_to_context =  True,
    )