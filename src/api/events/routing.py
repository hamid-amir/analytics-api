from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from .models import (
    EventModel,
    EventListSchema, 
    EventBucketSchema,
    EventCreateShema, 
    EventStatus,
    get_utc_now
)
from sqlmodel import Session, delete, select, func, case
from timescaledb.hyperfunctions import time_bucket
from api.db.session import get_session


DEFAULT_LOOKUP_PAGES = [
        "/", "/about", "/pricing", "/contact", 
        "/blog", "/products", "/login", "/signup",
        "/dashboard", "/settings"
    ]


router = APIRouter()

@router.get("/", response_model=List[EventBucketSchema])
def read_events(
    duration: str = Query(default="1 day"),
    pages: list[str] = Query(default=None),
    session:Session = Depends(get_session)
    ):
    os_case = case(
        (EventModel.user_agent.ilike('%windows%'), 'Windows'),
        (EventModel.user_agent.ilike('%macintosh%'), 'MacOS'),
        (EventModel.user_agent.ilike('%iphone%'), 'iOS'),
        (EventModel.user_agent.ilike('%android%'), 'Android'),
        (EventModel.user_agent.ilike('%linux%'), 'Linux'),
        else_='Other'
    ).label('operating_system')

    bucket = time_bucket(duration, EventModel.time)
    desired_pages = pages if isinstance(pages, list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES
    query = (
        select(
            bucket.label("bucket"),
            os_case,
            EventModel.page.label("page"),
            func.avg(EventModel.duration).label("avg_duration"),
            func.count().label("count")
        )
        .where(
            EventModel.page.in_(desired_pages)
        )
        .group_by(
            bucket,
            os_case,
            EventModel.page
        )
        .order_by(
            bucket,
            os_case,
            EventModel.page,
        )
    )
    results = session.exec(query).fetchall()
    return results


@router.get("/{event_id}", response_model=EventModel)
def read_events(
    event_id: int,
    session:Session = Depends(get_session)
    ):
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found in the database!")
    return result


@router.post("/", response_model=EventModel)
def create_events(
    payload:EventCreateShema,
    session:Session = Depends(get_session)
    ):
    data = payload.model_dump()  # pydantic -> dict
    obj = EventModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


# @router.put("/{event_id}", response_model=EventModel)
# def update_events(
#     event_id:int, 
#     payload:EventUpdateShema,
#     session:Session = Depends(get_session)
#     ):
#     query = select(EventModel).where(EventModel.id == event_id)
#     obj = session.exec(query).first()
#     if not obj:
#         raise HTTPException(status_code=404, detail="Event not found in the database!")
#     data = payload.model_dump()
#     for k,v in data.items():
#         setattr(obj, k, v)
#     obj.updated_at = get_utc_now()
#     session.add(obj)
#     session.commit()
#     session.refresh(obj)
#     return obj


@router.delete("/{event_id}", response_model=EventStatus)
def delete_events(
    event_id:int,
    session:Session = Depends(get_session)
    ):
    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found in the database!")
    session.delete(obj)
    session.commit()
    return {
        "id": event_id,
        "status": "deleted from the database!"
    }