from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,

    )
    priority: Literal["高", "中", "低"] = "中"


class TaskResponse(TaskCreate):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: int
    completed: bool
class TaskDeleteResponse(BaseModel):
    message: str
    id: int