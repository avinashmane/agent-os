from team.solutioning import sol_team
from agno.tools.function import UserInputField
from typing import List
from agno.utils import pprint
# sol_team.cli_app()
run_response = sol_team.run("Can you estimate SAP implementation for FI,SD,MM for 100 programs, 200 reports, 150 interfaces, 20 workflows, 100 enhancements, 50 conversions?")

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

    run_response = sol_team.continue_run(  run_response=run_response,
                                        # run_id=run_response.run_id, 
                                        updated_tools=run_response.tools)

    # If the agent is not paused for input, we are done
    if not run_response.is_paused:
        pprint.pprint_run_response(run_response)
        break