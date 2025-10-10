from agno.agent.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.tools.user_control_flow import UserControlFlowTools
from dotenv import load_dotenv
load_dotenv()
from lib import get_model, env
from lib import get_db, get_vector_db
from box import Box

cfg=Box.from_yaml("""
desc: |
    You are obedient agent to create estimations for software ervices projects based on user requirements. 
                  
instructions: 
- check which offering it matches from knowledge base
- "You are an interactive assistant that can ask users for input when needed"
- "Use user input requests to gather specific information or clarify requirements"
- you should focus on services estimation, which will results in person hours
- Please answer from the knowledge base.  If you cant find please state not found
""")

with open(f"{env('ROOT')}/instructions/estimation_guidance.md", "r") as f:
    guidelines = f.read()

off_db=get_db(knowledge_table="offering_db")

chat_agent = Agent(
    name="Estimation2 Agent",
    model=get_model(),
    description=cfg.desc,
    # instructions=cfg.instructions,
    instructions=[
        "You are an interactive assistant that can ask users for input when needed",
        "Use user input requests to gather specific information or clarify requirements",
        "Always explain why you need the user input and how it will be used",
        "Provide clear prompts and instructions for user responses",
    ],
    additional_context=guidelines,
    tools=[UserControlFlowTools()],
    # knowledge=Knowledge(contents_db=off_db,
    #                     vector_db=get_vector_db(table_name="vectors")),
    # search_knowledge=True,    
    markdown=True,
    debug_mode=True
    )

# agent_os = AgentOS(agents=[chat_agent], interfaces=[AGUI(agent=chat_agent)])
# app = agent_os.get_app()

# if __name__ == "__main__":
#     agent_os.serve(app="basic:app", reload=True)