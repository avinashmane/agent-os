import asyncio
from agno.client import AgentOSClient

async def main():
    # Connect to AgentOS
    client = AgentOSClient(base_url="http://localhost:7777")

    # Get configuration and available agents
    config = await client.aget_config()
    print(f"Connected to: {config.name or config.os_id}")
    print(f"Available agents: {[a.id for a in config.agents]}")

    # Run an agent
    if config.agents:
        result = await client.run_agent(
            agent_id=config.agents[0].id,
            message="Hello, how can you help me?",
        )
        print(f"Response: {result.content}")

asyncio.run(main())