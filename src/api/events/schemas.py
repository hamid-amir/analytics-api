from typing import List, Optional
from pydantic import BaseModel, Field

class EventSchema(BaseModel):
    id: int
    page: Optional[str] = Field(default="")
    description: Optional[str] = Field(default="")


class EventCreateShema(BaseModel):
    path: str
    description: Optional[str] = Field(default="")


class EventUpdateShema(BaseModel):
    description: str


class EventListSchema(BaseModel):
    results: List[EventSchema]
    count: Optional[int]