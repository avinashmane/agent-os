from dotenv import load_dotenv
load_dotenv()
import os
from agno.team import Team
from agno.workflow import Step, Workflow, StepOutput
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.agent import Agent
from agno.tools.user_control_flow import UserControlFlowTools
from agno.knowledge.knowledge import Knowledge
from agno.os import AgentOS
from copy import copy

# Setup the database
from lib import get_db, get_vector_db, get_model
from agents import create_basic_agents
from agents.know_agent import rag_agent, knowledge as know_1

agents={}
basic_agents = create_basic_agents("agents/basic_agents.yaml")
agents = copy(basic_agents)

web_db=get_db(knowledge_table="web_db")
agents["web-agent"] = Agent(
    id="web-agent",
    name="Web Research Agent",
    model=get_model(),
    db=web_db,
    tools=[DuckDuckGoTools()],#
    add_history_to_context=True,
    num_history_runs=3,
    enable_session_summaries=True ,
    instructions="Please answer from the knowledge base.  If you cant find please state not found",
    knowledge=Knowledge(contents_db=web_db,
                        vector_db=get_vector_db(table_name="test_vector")),
    knowledge_filters={"agent":"web-agent"},
    search_knowledge=True,
    markdown=True,
)


from agno.agent import Agent
from agno.tools.user_control_flow import UserControlFlowTools

agents['fit'] = Agent(
    model=get_model(),
    id="user-input",
    name='User input',
    instructions=[
        "You are an interactive assistant that can ask users for input when needed",
        "Use user input requests to gather specific information or clarify requirements",
        "Always explain why you need the user input and how it will be used",
        "Provide clear prompts and instructions for user responses",
    ],
    tools=[UserControlFlowTools()],
)

# agent.print_response("Help me create a personalized workout plan", stream=True)

agents["knowledgeagent"] = rag_agent

# workflow = Workflow(
#     name="ROM Solutioning Pipeline",
#     steps=basic_agents,
# )

from team.solutioning import sol_team
from tools.resources import save_resource_plan
rom_solutioning_team = Team(
    id="rom-solutioning-team",
    name="ROM Solution Team",
    model=get_model(),
    description="create pricing from the resource plan create from the detailed estimate...in the workflow",
    instructions=[
        "create detailed estimation in terms of person months from the user inputs",
        "create detailed resource from from the detailed estimate",
        "create pricing from the detailed resource plan"
    ],
    add_session_state_to_context=True,
    enable_agentic_state=True,
    tools=[save_resource_plan,UserControlFlowTools()],
    # external_execution=True ,
    db=get_db(),
    members=basic_agents.values(),
    add_history_to_context=True,
    num_history_runs=3,
    )



print(agents.keys())
config_file_path = f"{os.path.dirname(__file__)}/agentos_config.yaml"

from agents.demo_agent_state import agent as state_agent
from agents.demo_imagegen import image_agent
agent_os = AgentOS(
    os_id="my-Solutioning-os",
    description="My Solutioning AgentOS",
    teams=[sol_team, rom_solutioning_team],
    # workflows=[workflow],
    agents=[image_agent, state_agent,*agents.values()],
    config=config_file_path,
)

app = agent_os.get_app()

if __name__ == "__main__":
    # Default port is 7777; change with port=...
    agent_os.serve(app="main_agentos:app", reload=True)