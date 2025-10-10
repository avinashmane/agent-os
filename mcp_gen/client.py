"""MCP Streamable HTTP Client"""
"ref https://medium.com/google-cloud/model-context-protocol-mcp-with-google-gemini-llm-a-deep-dive-full-code-ea16e3fac9a3"

import argparse
import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from dotenv import load_dotenv
load_dotenv()
from rich.console import Console
from rich.markdown import Markdown
import os
# print(os.getenv("GEMINI_API_KEY"))

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from google import genai
from google.genai import types



class MCPClient:
    """MCP Client for interacting with an MCP Streamable HTTP server"""
    model="gemini-2.5-flash"

    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.client = genai.Client()
        self.chat = self.client.chats.create(model=self.model)
        self.console=Console()
        self.print=self.console.print
                

    async def connect_to_streamable_http_server(
        self, server_url: str, headers: Optional[dict] = None
    ):
        """Connect to an MCP server running with HTTP Streamable transport"""
        self._streams_context = streamablehttp_client(  # pylint: disable=W0201
            url=server_url,
            headers=headers or {},
        )
        read_stream, write_stream, _ = await self._streams_context.__aenter__()  # pylint: disable=E1101

        self._session_context = ClientSession(read_stream, write_stream)  # pylint: disable=W0201
        self.session: ClientSession = await self._session_context.__aenter__()  # pylint: disable=C2801

        await self.session.initialize()

    async def process_query(self, query: str) -> str:
        """Process a query using Claude and available tools"""
        messages = [{"role": "user", "content": query}]
        
        mcp_tools = await self.session.list_tools()

        tools = mcp_tools_to_tools(mcp_tools)

        config = types.GenerateContentConfig(temperature= 0, tools= tools)#[self.session])#

        # Initial LLM API call
        # print("Available tools:", [tool.name for tool in mcp_tools.tools])
        
        response = self.chat.send_message(
            query,
            config=config
        )

        # Process response and handle tool calls
        final_text = []

        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            if part.thought:
                print("Thought summary:")
                print(part.text)
                print()
            if part.executable_code is not None:
                print(part.executable_code.code)
            if part.code_execution_result is not None:
                print(part.code_execution_result.output)
            if part.function_call is not None:
                print("Function call:",part.function_call)
                # for tool_call in part.function_call:
                tool_call=part.function_call

                tool_name = tool_call.name
                tool_args = tool_call.args
                
                # Execute tool call
                result = await self.session.call_tool(tool_name, tool_args)

                final_text.append(f"__[Calling tool {tool_name} with args {tool_args}]__")
                # Continue conversation with tool results
                # if hasattr(part, "text") and part.text:
                #     messages.append({"role": "assistant", "content": part.text})
                # messages.append({"role": "user", "content": result.content})

                # Get next response from LLM
                response = self.chat.send_message(
                    self.combined_prompt(query, result)
                )

                # print("Next response:",response)
                for i,part in enumerate(response.candidates[0].content.parts):   
                    if part.text is not None:
                        final_text.append(part.text)
                    else:
                        final_text.append("[No text in response part]",i)

        return "\n\n".join(final_text)

    def combined_prompt(self, query, result):
        x= f"{query} \n {self.text_from_mcp_result(result)}"
        # print(x )
        return x

    def text_from_mcp_result(self, result):
        # print(result)
        if result and result.content:
            for content in result.content:
                if content.type == "text" and content.text:
                    return content.text

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == "quit":
                    break

                response = await self.process_query(query)
                self.print(Markdown("\n" +response), soft_wrap=True)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Properly clean up the session and streams"""
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if self._streams_context:  # pylint: disable=W0125
            await self._streams_context.__aexit__(None, None, None)  # pylint: disable=E1101

def mcp_tools_to_tools(mcp_tools):
    return [
    types.Tool(
        function_declarations=[
        {
            "name": tool.name,
            "description": tool.description,
            "parameters": {
            k: v
            for k, v in tool.inputSchema.items()
            if k not in ["additionalProperties", "$schema"]
            },
        }
        ]
    )
    for tool in mcp_tools.tools
]


async def main():
    """Main function to run the MCP client"""
    parser = argparse.ArgumentParser(description="Run MCP Streamable http based Client")
    parser.add_argument(
        "--mcp-localhost-port", type=int, default=8123, help="Localhost port to bind to"
    )
    args = parser.parse_args()

    client = MCPClient()

    try:
        await client.connect_to_streamable_http_server(
            f"http://localhost:{args.mcp_localhost_port}/mcp"
        )
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())