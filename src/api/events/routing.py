from fastapi import APIRouter
from .schemas import (
    EventSchema, 
    EventListSchema, 
    EventCreateShema, 
    EventUpdateShema
)

router = APIRouter()


@router.get("/")
def read_events() -> EventListSchema:
    return {
        "results": [
            {"id":1}, {"id":2}, {"id":3}
        ],
        "count": 3
    }


@router.get("/{event_id}")
def read_events(event_id: int) -> EventSchema:
    return {
        "id": event_id
    }


@router.post("/")
def create_events(payload:EventCreateShema) -> EventSchema:
    # print(payload)
    data = payload.model_dump()
    return {
        "id": 123,
        **data
    }


@router.put("/{event_id}")
def update_events(event_id:int, payload:EventUpdateShema) -> EventSchema:
    print(payload)
    return {
        "id": event_id
    }