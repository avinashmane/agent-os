from agno.models.google import Gemini 
from agno.models.ollama import Ollama
import os

def get_model(
        id=os.environ.get("MODEL", "gemini-2.0-flash-001")
        ):
    m_id=id.split("/").pop()
    if id.startswith("gemini"):
        return Gemini(id=m_id)
    else:
        return Ollama(id=m_id)

model= get_model()
