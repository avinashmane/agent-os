from agno.agent import Agent
from agno.tools.file import FileTools
from agno.tools.brandfetch import BrandfetchTools
from lib import get_model
api_key="1idQHP5EtHNptoZiEt3"
base_dir="./instructions"
agent = Agent(model=get_model(),tools=[FileTools(base_dir=base_dir),BrandfetchTools(api_key=api_key)]) #
# "What is the most advanced LLM currently? Save the answer to a file.",
agent.cli_app( markdown=True, stream=True)