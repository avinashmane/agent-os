"""Staffing resources for MCP servers.

This module exports resource functions and a `register(mcp_obj)` helper so a
calling server can attach the resources to its `FastMCP` instance. Do not rely
on an `mcp` global being present in this module's namespace.
"""


from typing import Any
from mcp.server.fastmcp.prompts import base

def read_document(name: str) -> str:
  """Read a document by name.

  In a real implementation this would read from disk or another storage
  backend. The resource URI for this will be `file://documents/{name}`.
  """
  return f"Content of {name}"


def get_settings() -> str:
  """Return application settings as JSON string.

  The resource URI for this will be `config://settings`.
  """
  return """{
  "theme": "dark",
  "language": "en",
  "debug": false
}"""


async def create_resource_plan(id: str, resource_needs: dict) -> dict:
    """Create a resource plan dataframe based on resource needs.

    Args:
        id: unique identified
        resource_needs: A dictionary describing the resource needs, e.g., {"role": "developer", "count": 2, "duration_months": 6}.
    """
    import pandas as pd

    # Example: Convert resource_needs to a DataFrame
    # In a real scenario, this would involve more complex logic
    # to generate a detailed resource plan.
    df = pd.DataFrame([resource_needs])
    return df.to_dict(orient="records")

def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

def register(mcp_obj):
  """Register staffing resources on the given FastMCP instance.

  Example:
    from mcp.server.fastmcp import FastMCP
    import staffing

    mcp = FastMCP(name="mytools")
    staffing.register(mcp)

  The function attaches the resource decorators at runtime so callers can
  control which `mcp` instance owns the resources.
  """
  mcp_obj.resource("file://documents/{name}")(read_document)
  mcp_obj.resource("config://settings")(get_settings)
  mcp_obj.tool()(create_resource_plan)
  mcp_obj.prompt(title="Debug Assistant")(debug_error)

  return mcp_obj


