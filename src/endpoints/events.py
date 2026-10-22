

from fastapi import APIRouter

from src.db.queries.events import EventQueries
from src.models.events import EventListResponse

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("", response_model=EventListResponse)
async def get_all_events():
    events = await EventQueries.get_all(order_by="id")
    response = {
        "events": events
    }
    return response