from typing import List, Optional
# from pydantic import BaseModel, Field
import sqlmodel
from sqlmodel import SQLModel, Field, table
from datetime import datetime, timezone



def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)


class EventModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    page: Optional[str] = Field(default="")
    description: Optional[str] = Field(default="")
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=True
    )



class EventCreateShema(SQLModel):
    path: str
    description: Optional[str] = Field(default="")


class EventUpdateShema(SQLModel):
    description: str


class EventListSchema(SQLModel):
    results: List[EventModel]
    count: Optional[int]


class EventStatus(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: Optional[str] = Field(default=None, primary_key=True)