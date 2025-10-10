from typing import List
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.function import UserInputField
from agno.tools import tool
from agno.utils import pprint
from agno.tools.user_control_flow import UserControlFlowTools
# We still provide a docstring to the tool; This will be used to populate the `user_input_schema`
@tool(requires_user_input=True)
def send_email(to: str, subject: str, body: str) -> dict:
    """Send an email to the user.

    Args:
        to (str): The address to send the email to.
        subject (str): The subject of the email.
        body (str): The body of the email.
    """
    # Implementation here
    return f"Email sent to {to} with subject {subject} and body {body}"

agent = Agent(
    model=Gemini(id="gemini-2.5-flash"),
    instructions="Ask for any missing inputs",
    tools=[send_email,UserControlFlowTools()],
    debug_mode=True
)

run_response = agent.run("Send an email to avinash@yahoo.com please")
print(run_response)
if run_response.is_paused:
    
    for tool in run_response.tools_requiring_user_input:
        input_schema: List[UserInputField] = tool.user_input_schema

        for field in input_schema:
            # Display field information to the user
            print(f"\nField: {field.name} ({field.field_type.__name__}) -> {field.description}")

            # Get user input
            user_value = input(f"Please enter a value for {field.name}: ")

            # Update the field value
            field.value = user_value

    run_response = (
        agent.continue_run(run_response=run_response,#run_id=run_response.run_id, 
                           updated_tools=run_response.tools)
    )
    pprint.pprint_run_response(run_response)