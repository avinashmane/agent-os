
import asyncio
from agno.client.a2a import A2AClient

async def main():
    # Connect to an Agno AgentOS A2A endpoint
    client = A2AClient("http://localhost:7777/a2a/agents/my-agent")

    # Send a message
    result = await client.send_message(message="Hello! what is price for TSLA")
    print(result.content)

asyncio.run(main())