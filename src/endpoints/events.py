

from fastapi import APIRouter

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("")
async def get_all_events():
    return [{"id": 1, "name": "Event 1"}, {"id": 2, "name": "Event 2"}]