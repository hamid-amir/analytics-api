from typing import List, Optional
# from pydantic import BaseModel, Field
import sqlmodel
from sqlmodel import SQLModel, Field, table
from datetime import datetime, timezone
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now



class EventModel(TimescaleModel, table=True):
    page: str = Field(index=True)
    user_agent: Optional[str] = Field(default="", index=True)
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True)
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default=0)

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months"



class EventCreateShema(SQLModel):
    page: str
    user_agent: Optional[str] = Field(default="", index=True)
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True)
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default=0)


# class EventUpdateShema(SQLModel):
#     description: str


class EventListSchema(SQLModel):
    results: List[EventModel]
    count: Optional[int]


class EventBucketSchema(SQLModel):
    bucket: datetime
    page: str
    count: int
    operating_system: Optional[str] = ""
    avg_duration: Optional[float] = 0.0


class EventStatus(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: Optional[str] = Field(default=None, primary_key=True)