"""Weather tools for MCP Streamable HTTP server using NWS API."""

import argparse
from typing import Any
from contextlib import asynccontextmanager

import ngrok
import httpx
import uvicorn
from os import getenv
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from loguru import logger
NGROK_AUTH_TOKEN = getenv("NGROK_AUTH_TOKEN", "")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run MCP Streamable HTTP based server")
    parser.add_argument("--port", type=int, default=8123, help="Localhost port to listen on")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host name to bind service to")
    args = parser.parse_args()

    @asynccontextmanager
    async def lifespan(app: FastMCP):  #: FastAPI
        logger.info(f"Setting up ngrok Endpoint with {NGROK_AUTH_TOKEN}")
        ngrok.set_auth_token(NGROK_AUTH_TOKEN)
        ngrok.forward(
            addr=args.port,
        )
        yield
        logger.info("Tearing Down ngrok Endpoint")
        ngrok.disconnect()

    # Initialize FastMCP server for Weather tools.
    # If json_response is set to True, the server will use JSON responses instead of SSE streams
    # If stateless_http is set to True, the server uses true stateless mode (new transport per request)
    security_settings=TransportSecuritySettings(allowed_hosts=["*","firm-swan-prompt.ngrok-free.app", "localhost:8123", "localhost"])

    mcp = FastMCP(name="weather", json_response=False, stateless_http=False, transport_security=security_settings)# lifespan=lifespan)

    
    import weather

    weather.register(mcp)

    import staffing
    staffing.register(mcp)

    @mcp.tool()
    async def get_duration(efforts: float, est_type: str) -> float:
        """Get duration of the project based on efforts.

        Args:
            efforts: efforts in person months
            est_type: Esitmation type. CS for implementation and AMS for support
        """
        from math import sqrt
        factor=1.1
        return round(sqrt(efforts)/factor,0)

    from starlette.applications import Starlette
    from starlette.routing import Mount, Route
    from starlette.responses import PlainTextResponse
    async def homepage(request):
        return PlainTextResponse("Homepage")

    async def about(request):
        return PlainTextResponse("About")

    # app=mcp.streamable_http_app( )
    # app=mcp.sse_app(mount_path='/mcp-avi')
    app = Starlette(
        routes=[
            # Using settings-based configuration
            Mount("/mcp-avi", app=mcp.sse_app()),
            Route("/", endpoint=homepage),
            Route("/about", endpoint=about),
    ])
    
    logger.info(f"Starting with Streamable HTTP transport at {args.host}:{args.port}")


    # Start the server with Streamable HTTP transport
    uvicorn.run( app, host=args.host, port=args.port,  )