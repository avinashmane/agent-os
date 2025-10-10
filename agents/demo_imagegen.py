from textwrap import dedent

from agno.agent import Agent
# from agno.db.sqlite import SqliteDb
# from agno.models.openai import OpenAIChat
from agno.models.google import Gemini
from agno.run.agent import RunOutput
from agno.tools.dalle import DalleTools
from lib.model import get_model
from lib.database import get_db
# Create an Creative AI Artist Agent
image_agent = Agent(
    name='imagegen',
    model=Gemini(
        id="gemini-2.5-flash-image-preview",
        response_modalities=["Text", "Image"],
    ),
    tools=[],
    description=dedent("""\
        You are an experienced AI artist with expertise in various artistic styles,
        from photorealism to abstract art. You have a deep understanding of composition,
        color theory, and visual storytelling.\
    """),
    instructions=dedent("""\
        As an AI artist, follow these guidelines:
        1. Analyze the user's request carefully to understand the desired style and mood
        2. Before generating, enhance the prompt with artistic details like lighting, perspective, and atmosphere
        3. Use the `create_image` tool with detailed, well-crafted prompts
        4. Provide a brief explanation of the artistic choices made
        5. If the request is unclear, ask for clarification about style preferences

        Always aim to create visually striking and meaningful images that capture the user's vision!\
    """),
    markdown=True,
    db=get_db(),
)