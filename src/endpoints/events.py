

from fastapi import APIRouter

from src.db.queries.events import EventQueries
from src.exceptions import NCPlusOneHTTPException
from src.models.events import EventListResponse, EventResponse, SingleEventResponse

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("", response_model=EventListResponse)
async def get_all_events():
    events = await EventQueries.get_all(order_by="id")
    response = {
        "events": events
    }
    return response

@router.get("/{event_id}", response_model=SingleEventResponse)
async def get_event_by_id(event_id: int):
    event = await EventQueries.get_by_id(event_id)
    if not event:
        raise NCPlusOneHTTPException(status_code=404, detail="Event not found")
    response = {
        "event": event
    }
    return response