from agno.tools.mcp import MCPTools
from agno.agent import Agent
from lib import get_model,env
from box import Box

cfg=Box.from_yaml("""
desc: |
    You are obedient agent to create resource plan for software ervices projects based efforts and duration. 
instructions: 
- calculate the duration only of not provided by user
- Ask for any missing inputs
- you should focus on services estimation, which will results in person hours

""")
with open(f"{env('ROOT')}/instructions/resourcing_guidance.md", "r") as f:
    guidelines = f.read()

def create_mcp_agent(model,
                     transport="streamable-http",
                     url="http://localhost:8123/mcp"):
    # Create MCPTools instance
    mcp_tools = MCPTools(
        transport=transport, 
        url=url
    )

    # Create MCP-enabled agent
    agent = Agent(
        id="resourcing-agent",
        name="Resourcing Agent",
        model=get_model(),
        description=cfg.desc,
        instructions=cfg.instructions,
        additional_context=guidelines,
        tools=[mcp_tools],
    )
    return agent