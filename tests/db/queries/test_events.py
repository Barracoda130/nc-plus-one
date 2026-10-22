

import pytest_asyncio
import pytest

from src.db.connection import _close_connection_pool
from src.db.setup.seed import seed_database
from src.db.queries.events import EventQueries
from src.models.events import EventListResponse, EventResponse


@pytest.mark.asyncio
async def test_get_all_events():
    events = await EventQueries.get_all()
    assert len(events) > 0

    # Ensure the shape of the data is correct
    events_model_list = [EventResponse(**event) for event in events]
    assert True # If it doesn't throw an error then the test passed

@pytest.mark.asyncio
async def test_get_all_events_with_ordering():
    events_ordered = await EventQueries.get_all(order_by="title")
    events_unordered = await EventQueries.get_all()

    assert len(events_ordered) > 0
    assert len(events_unordered) == len(events_ordered)
    
    assert events_ordered != events_unordered  # They should not be the same order
    assert events_ordered == sorted(events_ordered, key=lambda x: x['title'])

    
@pytest.mark.asyncio
async def test_get_all_events_empty_database(empty_database):
    manager = empty_database("src.db.queries.events.get_connection")
    events = await EventQueries.get_all()
    assert events == []  # Should return an empty list when the database is empty
    manager.connection.fetch.assert_called_once_with("SELECT * FROM events;")  # Ensure the correct query was executed


