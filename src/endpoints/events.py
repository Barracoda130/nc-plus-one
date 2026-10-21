

from fastapi import APIRouter

from src.db.queries.events import EventQueries

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("")
async def get_all_events():
    events = await EventQueries.get_all()
    return events