from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class ProjectType(Enum):
    CS = "Implementation"
    AMS = "Application Maintenance Support"
    STR = "Strategy"

class Solution(BaseModel):
    client: str = Field(str, description="Full name of the client")
    id: str = Field(str, description="Valid email address")
    project_type: int = Field(ProjectType, description="Age of the user")
    scope: List[str] = Field(default_factory=list, description="User interests")
    created_at: datetime = Field(default_factory=datetime.now, description="When the user was created")

