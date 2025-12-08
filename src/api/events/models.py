from typing import List, Optional
# from pydantic import BaseModel, Field
import sqlmodel
from sqlmodel import SQLModel, Field, table
from datetime import datetime, timezone
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now



class EventModel(TimescaleModel, table=True):
    # id: Optional[int] = Field(default=None, primary_key=True)
    page: str = Field(index=True)
    description: Optional[str] = Field(default="")
    # created_at: datetime = Field(
    #     default_factory=get_utc_now,
    #     sa_type=sqlmodel.DateTime(timezone=True),
    #     nullable=False
    # )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=True
    )

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months"



class EventCreateShema(SQLModel):
    page: str
    description: Optional[str] = Field(default="")


class EventUpdateShema(SQLModel):
    description: str


class EventListSchema(SQLModel):
    results: List[EventModel]
    count: Optional[int]


class EventStatus(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: Optional[str] = Field(default=None, primary_key=True)