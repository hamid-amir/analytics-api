from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, delete, select
from .models import (
    EventModel,
    EventListSchema, 
    EventCreateShema, 
    EventUpdateShema,
    EventStatus,
    get_utc_now
)
from api.db.session import get_session



router = APIRouter()


@router.get("/", response_model=EventListSchema)
def read_events(
    session:Session = Depends(get_session)
    ):
    query = select(EventModel).order_by(EventModel.updated_at.asc()).limit(10)
    results = session.exec(query).all()
    return {
        "results": results,
        "count": len(results)
    }


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


@router.put("/{event_id}", response_model=EventModel)
def update_events(
    event_id:int, 
    payload:EventUpdateShema,
    session:Session = Depends(get_session)
    ):
    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found in the database!")
    data = payload.model_dump()
    for k,v in data.items():
        setattr(obj, k, v)
    obj.updated_at = get_utc_now()
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


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