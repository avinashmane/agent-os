
import asyncio
from agno.client.a2a import A2AClient

async def main():
    # Connect to an Agno AgentOS A2A endpoint
    client = A2AClient("http://localhost:8123/a2a/agents/my-agent")

    # Send a message
    for msg in ["What tools you have?","What is the price of TSLA","What is the price of TSLA in 2020"]:
        result = await client.send_message(message= msg)
        print(result.content)

asyncio.run(main())