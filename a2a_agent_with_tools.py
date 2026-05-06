from agno.agent.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIResponses
from agno.os import AgentOS
from agno.os.interfaces.a2a import A2A
# from agno.db.postgres import PostgresDb
from agno.registry import Registry
from agno.models.ollama import Ollama
from agno.tools.websearch import WebSearchTools
from agno.tools.yfinance import YFinanceTools
from textwrap  import dedent
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi import HTTPException
import argparse
from typing import Any
from contextlib import asynccontextmanager
import os
import ngrok
from loguru import logger
from dotenv import load_dotenv
import uvicorn
load_dotenv()

# os.environ
from lib import get_db, get_vector_db, get_model, get_knowledge_base

# Create your custom FastAPI app
app = FastAPI(title="My Custom App", debug=True)

@app.get("/home")
async def homepage():
    return HTMLResponse(dedent("""
                    Homepage:
                    A2A: http://localhost:8123/sse-stream/
                    MCP: http://localhost:8123/mcp-srv
                    """))

@app.get("/about")
async def about():
    return HTMLResponse("About")
#++++++ studio

db_url=os.getenv("DB_URL")
db = get_db()#PostgresDb(db_url=db_url)


#------
from schemas.solution import Solution

#+++ agents local
from agents.finance import agent as finance_agent

#+++ teams resources
from team.solutioning import sol_team
from tools.resources import save_resource_plan

knowledgebases = [get_knowledge_base(x) for x in [
 "offerings",
 "past-solutions",
 "jrs",
 "product-catalog"
]]

registry = Registry(
    name="My Registry",
    tools=[WebSearchTools(), YFinanceTools(),],
    models=[get_model(),Ollama(id="lfm2.5-thinking:latest")],
    dbs=[db], #Studio requires the `db` parameter to save and load agents, teams, and workflows.
    schemas=[Solution],
    functions=[save_resource_plan]
    
)

# agent OS with A2A
agent_os = AgentOS(
    id="my-app",
    db=db,
    registry=registry,
    agents=[finance_agent],
    teams=[sol_team],
    knowledge=knowledgebases,
    a2a_interface=True,
    base_app=app,
    # enable_mcp_server=True,
    run_hooks_in_background=False
)
app = agent_os.get_app()


@app.get("/instructions/{filename}")
def download_instruction(filename: str):
    file_path = os.path.join(os.getenv("ROOT", "."), "instructions", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")


# # Mount MCP under /mcp-srv to avoid conflict with AgentOS internals
# from mcp_gen.server import mcp

# def map_mcp_on_fastapi_app(mcp,app):
#         ##++++++++ MCP start
#         from fastapi import FastAPI, Request
#         from mcp.server.sse import SseServerTransport
#         from starlette.routing import Mount
        
#         # Create SSE transport instance for handling server-sent events
#         sse = SseServerTransport("/messages/")
        
#         # Mount the /messages path to handle SSE message posting
#         app.router.routes.append(Mount("/messages", app=sse.handle_post_message))
        
        
#         # Add documentation for the /messages endpoint
#         @app.post("/messages", tags=["MCP"], include_in_schema=True)
#         def messages_docs():
#             """
#             Messages endpoint for SSE communication
        
#             This endpoint is used for posting messages to SSE clients.
#             Note: This route is for documentation purposes only.
#             The actual implementation is handled by the SSE transport.
#             """
#             pass  # This is just for documentation, the actual handler is mounted above
        
        
#         @app.get("/sse", tags=["MCP"])
#         async def handle_sse(request: Request):
#             """
#             SSE endpoint that connects to the MCP server
        
#             This endpoint establishes a Server-Sent Events connection with the client
#             and forwards communication to the Model Context Protocol server.
#             """
#             # Use sse.connect_sse to establish an SSE connection with the MCP server
#             async with sse.connect_sse(request.scope, request.receive, request._send) as (
#                 read_stream,
#                 write_stream,
#             ):
#                 # Run the MCP server with the established streams
#                 await mcp._mcp_server.run(
#                     read_stream,
#                     write_stream,
#                     mcp._mcp_server.create_initialization_options(),
#                 )
#         pass 

    
if __name__ == "__main__":
    # agent_os.serve(app="a2a_agent_with_tools:app", reload=True, port=8123)
    
    parser = argparse.ArgumentParser(description="Run AgentOS+A2A+MCP based server")
    parser.add_argument("--port", type=int, default=8123, help="Localhost port to listen on")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host name to bind service to")
    args = parser.parse_args()

    # @asynccontextmanager
    # async def lifespan(app: FastMCP):  #: FastAPI
    #     logger.info(f"Setting up ngrok Endpoint with {NGROK_AUTH_TOKEN}")
    #     ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    #     ngrok.forward(
    #         addr=args.port,
    #     )
    #     yield
    #     logger.info("Tearing Down ngrok Endpoint")
    #     ngrok.disconnect()


    # from starlette.applications import Starlette
    # from starlette.routing import Mount, Route
    # from starlette.responses import PlainTextResponse

    # app=mcp.streamable_http_app( )
    # app=mcp.sse_app(mount_path='/mcp-avi')
    # app = Starlette(
    #     routes=[
    #         # Using settings-based configuration
    #         Mount("/mcp", app=mcp.sse_app()),
    #         Route("/home", endpoint=homepage),
    #         Route("/about", endpoint=about),
    # ])
    
    
    # map_mcp_on_fastapi_app(mcp,app)
    # from starlette.applications import Starlette
    # from starlette.routing import Mount
    # from starlette.middleware.trustedhost import TrustedHostMiddleware
    
    # # mcp_starlette_app = mcp.sse_app()
    
    # top_app = Starlette(
    #     routes=[
    #         # Mount("/mcp", app=mcp_starlette_app),
    #         Mount("/", app=app),
    #     ]
    # )
    # top_app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "firm-swan-prompt.ngrok-free.app"])

    ##--------- MCP end
    logger.info(f"Starting with at {args.host}:{args.port}", )


    # Start the server 
    uvicorn.run( app, host=args.host, port=args.port,  )

