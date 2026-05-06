import os

model_id=os.environ.get("MODEL", "gemini-2.0-flash-001")
print(f"MODEL={model_id}")

def get_model(
        id=model_id
        ):
    m_id=id.split("/").pop()
    if id.startswith("gemini"):
        from agno.models.google import Gemini 
        return Gemini(id=m_id)
    elif id.startswith("global"):
        from agno.models.openai import  OpenAILike
        return OpenAILike(id=id, 
                base_url=os.getenv("OPENAI_API_BASE"), 
                api_key=os.getenv("OPENAI_API_KEY"))
    else:
        from agno.models.ollama import Ollama
        return Ollama(id=m_id)

model= get_model()
