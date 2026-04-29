from agno.agent.agent import Agent
from agno.tools.user_control_flow import UserControlFlowTools
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))
from lib.model import get_model
import yaml
from box import box_from_file
import os
from lib import  get_db
from lib.text_utils import get_text


db=get_db()

def create_basic_agents(file_name,
            enable_user_memories=True,
            add_session_state_to_context=True,  # Required so the agent is aware of the session state
            enable_agentic_state=True,  # Adds a tool to manage the session state
            markdown=True,
            debug_mode=True):
    # with open(file_name, "r") as f:
    #     agent_data = yaml.safe_load(f.read())

    agent_data=box_from_file(f"{os.getenv('AGENTS_DIR', '.')}/{file_name}")

    agents={}

    for name,agent_info in agent_data.items():
        agent_id = name.strip().lower().replace(" ","-")
        if not agent_id:
            continue
        agent_description = agent_info.get('persona')+"\n\n\nyou goal is:\n"+agent_info.get('goals', "")
        expected_output=agent_data.get("expected_output" , None)

        instruction_path=f"{os.getenv('ROOT')}/instructions"

        inst_path = f"{instruction_path}/{agent_info.get('instructions', None)}"
        agent_instructions = get_text(inst_path)

        agents[agent_id] = Agent(
            name=name,
            db=db,
            model=get_model(),
            add_history_to_context=True,
            num_history_runs=3,
            # tools=[UserControlFlowTools()],
            description=agent_description,  
            instructions=agent_instructions,
            expected_output=expected_output,
            enable_user_memories=enable_user_memories,
            enable_agentic_memory=True, 
            add_session_state_to_context=add_session_state_to_context,
            enable_agentic_state=enable_agentic_state,
            # external_execution=True ,
            markdown=markdown,
            debug_mode=debug_mode
        )

    return agents