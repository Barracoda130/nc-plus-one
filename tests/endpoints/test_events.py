
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

@pytest.mark.asyncio
async def test_get_event_by_id(async_client):
    async with async_client as client:
        response = await client.get("/api/events/1") 
        
    assert response.status_code == 200
    data = response.json()
    assert "event" in data
    assert isinstance(data["event"], dict)
    
    event_from_db = await EventQueries.get_by_id(1)
    assert event_from_db is not None
    
    for key, value in event_from_db.items():
        if isinstance(value, datetime):
            event_from_db[key] = value.isoformat().replace("+00:00", "Z")  # Convert datetime to string for comparison

    assert event_from_db == data["event"]

@pytest.mark.asyncio
async def test_get_event_by_id_not_found(async_client):
    async with async_client as client:
        response = await client.get("/api/events/9999")  # Assuming this ID does not exist
        
    assert response.status_code == 404
    
@pytest.mark.asyncio
async def test_get_event_by_id_invalid_id(async_client):
    async with async_client as client:
        response = await client.get("/api/events/invalid")  # Invalid ID
        
    assert response.status_code == 422
    assert "error" in response.json()["detail"]