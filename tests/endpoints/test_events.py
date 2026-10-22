
import pytest
from datetime import datetime

from src.db.queries.events import EventQueries
from src.db.connection import _close_connection_pool

@pytest.mark.asyncio
async def test_get_all_events(async_client):
    async with async_client as client:
        response = await client.get("/api/events") 
        
    assert response.status_code == 200
    data = response.json()
    assert "events" in data
    assert isinstance(data["events"], list)
    
    events_from_db = await EventQueries.get_all(order_by="id")
    for event in events_from_db:
        for key, value in event.items():
            if isinstance(value, datetime):
                event[key] = value.isoformat().replace("+00:00", "Z")  # Convert datetime to string for comparison

    assert events_from_db == data["events"]