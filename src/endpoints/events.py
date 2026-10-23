

import asyncpg
from fastapi import APIRouter, Depends

from src.db.queries.events import EventQueries
from src.db.queries.rsvps import RSVPQueries
from src.endpoints.auth import get_current_user_id
from src.exceptions import NCPlusOneHTTPException
from src.db.exceptions import DatabaseError
from src.models.events import EventListResponse, EventResponse, SingleEventResponse
from src.models.rsvps import SingleRSVPResponse

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

@router.post("/{event_id}/rsvp", response_model=SingleRSVPResponse)
async def rsvp_to_event(event_id: int, user_id: int = Depends(get_current_user_id)):
    event = await EventQueries.get_by_id(event_id)
    
    if not event:
        raise NCPlusOneHTTPException(status_code=404, detail="Event not found")

    rsvp = await RSVPQueries.create_rsvp(event_id, user_id)

    response = {
        "rsvp": dict(rsvp)
    }
    
    return response

@router.delete("/{event_id}/rsvp/me", status_code=204, response_model=None)
async def delete_rsvp(event_id: int, user_id: int = Depends(get_current_user_id)):
    event = await EventQueries.get_by_id(event_id)
    
    if not event:
        raise NCPlusOneHTTPException(status_code=404, detail="Event not found")

    rsvp = await RSVPQueries.get_rsvp(event_id, user_id)
    if not rsvp:
        raise NCPlusOneHTTPException(status_code=404, detail="RSVP not found")

    await RSVPQueries.delete_rsvp(event_id, user_id)