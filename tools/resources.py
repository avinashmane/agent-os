import pandas as pd
from agno.tools import tool
from typing import Any, Callable, Dict, List
from pydantic import BaseModel

# class resourceAllocation(BaseModel):
    
class ResourceLine(BaseModel):
    role: str
    skill: str
    skill_level: str
    band: str
    location: str
    start_month: str
    allocation: List[float]

class ResourcePlan(BaseModel):
    project: str
    duration_months: int
    resources: List[ResourceLine]



def logger_hook(function_name: str, function_call: Callable, arguments: Dict[str, Any]):
    """Hook function that wraps the tool execution"""
    print(f"About to call {function_name} with arguments: {arguments}")
    result = function_call(**arguments)
    print(f"Function call completed with result: {result}")
    return result

PATH='tmp'

@tool(tool_hooks=[logger_hook],)
def save_resource_plan(resource_plan: ResourcePlan) -> str:
    """
    Save resource plan for later

    args:
    - resource_plan: pandas.DataFrame: 

    return files name
    """
    if isinstance(resource_plan, ResourcePlan):
        print(resource_plan)
        resource_plan.to_excel(f"{PATH}/temp.xlsx")
        return 'temp'
    else:
        print('Did not receive a dataframe')

@tool(tool_hooks=[logger_hook],)
def read_resource_plan(id: str) -> pd.DataFrame:
    """
    Read resource plan from prior session

    args:
    - id: files name: 

    return: resource_plan: pandas.DataFrame: 
    """
    if isinstance(id, str):
        df=pd.read_excel(f"{PATH}/temp.xlsx")
        return df
    else:
        print('Did not receive a dataframe')        