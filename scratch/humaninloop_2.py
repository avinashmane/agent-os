from typing import List
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.function import UserInputField
from agno.tools import tool
from agno.utils import pprint
from typing import Any, Dict


from agno.tools.toolkit import Toolkit
from agno.tools.user_control_flow import UserControlFlowTools

# Example toolkit for handling emails
class EmailTools(Toolkit):
    def __init__(self, *args, **kwargs):
        super().__init__(
            name="EmailTools", tools=[self.send_email, self.get_emails], *args, **kwargs
        )

    def send_email(self, subject: str, body: str, to_address: str) -> str:
        """Send an email to the given address with the given subject and body.

        Args:
            subject (str): The subject of the email.
            body (str): The body of the email.
            to_address (str): The address to send the email to.
        """
        return f"Sent email to {to_address} with subject {subject} and body {body}"

    def get_emails(self, date_from: str, date_to: str) -> str:
        """Get all emails between the given dates.

        Args:
            date_from (str): The start date.
            date_to (str): The end date.
        """
        return [
            {
                "subject": "Hello",
                "body": "Hello, world!",
                "to_address": "test@test.com",
                "date": date_from,
            },
            {
                "subject": "Random other email",
                "body": "This is a random other email",
                "to_address": "john@doe.com",
                "date": date_to,
            },
        ]


agent = Agent(
    model=Gemini(id="gemini-2.5-flash"),
    tools=[EmailTools(), UserControlFlowTools()],
    markdown=True,
    debug_mode=True,
)

run_response = agent.run("Send an email with the body 'How is it going in Tokyo?'")

# We use a while loop to continue the running until the agent is satisfied with the user input
while run_response.is_paused:
    for tool in run_response.tools_requiring_user_input:
        input_schema: List[UserInputField] = tool.user_input_schema

        for field in input_schema:
            # Display field information to the user
            print(f"\nField: {field.name} ({field.field_type.__name__}) -> {field.description}")

            # Get user input (if the value is not set, it means the user needs to provide the value)
            if field.value is None:
                user_value = input(f"Please enter a value for {field.name}: ")
                field.value = user_value
            else:
                print(f"Value provided by the agent: {field.value}")

    run_response = agent.continue_run(  run_response=run_response,
                                        # run_id=run_response.run_id, 
                                        updated_tools=run_response.tools)

    # If the agent is not paused for input, we are done
    if not run_response.is_paused:
        pprint.pprint_run_response(run_response)
        break