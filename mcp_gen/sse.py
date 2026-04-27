from starlette.applications import Starlette
from starlette.routing import Mount, Host
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
import uvicorn

security_settings=TransportSecuritySettings(allowed_hosts=["*","firm-swan-prompt.ngrok-free.app", "*.ngrok-free.app:*", "localhost"])
mcp = FastMCP("My App", transport_security=security_settings)

@mcp.tool()
def tool1():
    """
    Test test test
    """
    return 'adasdasda'



# Mount the SSE server to the existing ASGI server
app = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app( )),
    ]
)

# from starlette.applications import Starlette
# from starlette.routing import Mount
# from mcp.server.fastmcp import FastMCP
# import uvicorn

# # Create multiple MCP servers
# github_mcp = FastMCP("GitHub API")
# browser_mcp = FastMCP("Browser")
# curl_mcp = FastMCP("Curl")
# search_mcp = FastMCP("Search")

# # Method 1: Configure mount paths via settings (recommended for persistent configuration)
# github_mcp.settings.mount_path = "/github"
# browser_mcp.settings.mount_path = "/browser"

# # Method 2: Pass mount path directly to sse_app (preferred for ad-hoc mounting)
# # This approach doesn't modify the server's settings permanently

# # Create Starlette app with multiple mounted servers
# app = Starlette(
#     routes=[
#         # Using settings-based configuration
#         Mount("/github", app=github_mcp.sse_app()),
#         Mount("/browser", app=browser_mcp.sse_app()),
#         # Using direct mount path parameter
#         Mount("/curl", app=curl_mcp.sse_app("/curl")),
#         Mount("/search", app=search_mcp.sse_app("/search")),
#     ]
# )

# # Method 3: For direct execution, you can also pass the mount path to run()
# if __name__ == "__main__":
#     search_mcp.run(transport="sse", mount_path="/search")
#     # Run the Starlette app with all MCP mounts 
#     # This mounts the SSE transports at the configured mount paths
uvicorn.run(app, host="0.0.0.0", log_level="info")