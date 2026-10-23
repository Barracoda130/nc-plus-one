
import pytest
from datetime import datetime

from src.db.queries.events import EventQueries
from src.db.connection import _close_connection_pool
from src.models.events import EventListResponse, SingleEventResponse
from src.models.rsvps import SingleRSVPResponse
from tests.conftest import error_message_contains, is_error_response, login_user
from tests.endpoints.conftest import response_shape

class TestGetAllEvents:
    async def test_happy_path(self, async_client):
        async with async_client as client:
            response = await client.get("/api/events") 
            
        assert response.status_code == 200
        data = response.json()
        assert response_shape(data, EventListResponse)
        
        events_from_db = await EventQueries.get_all(order_by="id")
        for event in events_from_db:
            for key, value in event.items():
                if isinstance(value, datetime):
                    event[key] = value.isoformat().replace("+00:00", "Z")  # Convert datetime to string for comparison

        assert events_from_db == data["events"]
        
class TestGetEventById:
    async def test_happy_path(self, async_client):
        async with async_client as client:
            response = await client.get("/api/events/1") 
            
        assert response.status_code == 200
        data = response.json()
        assert response_shape(data, SingleEventResponse)
        
        event_from_db = await EventQueries.get_by_id(1)
        assert event_from_db is not None
        
        for key, value in event_from_db.items():
            if isinstance(value, datetime):
                event_from_db[key] = value.isoformat().replace("+00:00", "Z")  # Convert datetime to string for comparison

        assert event_from_db == data["event"]

    async def test_id_not_found(self, async_client):
        async with async_client as client:
            response = await client.get("/api/events/9999")  # Assuming this ID does not exist
            
        assert response.status_code == 404
        
    async def test_invalid_id(self, async_client):
        async with async_client as client:
            response = await client.get("/api/events/invalid")  # Invalid ID
            
        assert response.status_code == 422
        assert is_error_response(response.json())

class TestRSVPToEvent:
    async def test_happy_path(self, async_client, test_event, test_user):
        async with async_client as client:
            token = await login_user(client, test_user)
            print(f"Token: {token}")  # Debugging line to print the token
            response = await client.post(f"/api/events/{test_event['id']}/rsvp",
                                        headers={"Authorization": f"Bearer {token}"}
                                        )
            
        assert response.status_code == 200
        data = response.json()
        assert response_shape(data, SingleRSVPResponse)

        body = data["rsvp"]
        assert body["attendee_id"] == test_user["id"]
        assert body["event_id"] == test_event["id"]
        
    async def test_unauthorized(self, async_client, test_event):
        async with async_client as client:
            response = await client.post(f"/api/events/{test_event['id']}/rsvp")
            
        assert response.status_code == 401
        assert is_error_response(response.json())
        assert error_message_contains(response.json(), "Not authenticated")

    async def test_event_not_found(self, async_client, test_user):
        async with async_client as client:
            token = await login_user(client, test_user)
            response = await client.post(f"/api/events/9999/rsvp",  # Assuming this ID does not exist
                                        headers={"Authorization": f"Bearer {token}"}
                                        )
            
        assert response.status_code == 404
        assert is_error_response(response.json())
        assert error_message_contains(response.json(), "Event not found")
        
    async def test_rsvp_already_exists(self, async_client, test_event, test_user):
        async with async_client as client:
            token = await login_user(client, test_user)
            # First RSVP attempt
            response1 = await client.post(f"/api/events/{test_event['id']}/rsvp",
                                        headers={"Authorization": f"Bearer {token}"}
                                        )
            assert response1.status_code == 200
            
            # Second RSVP attempt (should fail)
            response2 = await client.post(f"/api/events/{test_event['id']}/rsvp",
                                        headers={"Authorization": f"Bearer {token}"}
                                        )
            
        assert response2.status_code == 409
        assert is_error_response(response2.json())
        assert error_message_contains(response2.json(), "RSVP already exists")

class TestDeleteRSVP:
    async def test_happy_path(self, async_client, test_event, test_user):
        async with async_client as client:
            token = await login_user(client, test_user)
            # First RSVP attempt
            response1 = await client.post(f"/api/events/{test_event['id']}/rsvp",
                                        headers={"Authorization": f"Bearer {token}"}
                                        )
            assert response1.status_code == 200
            
            # Now delete the RSVP
            response2 = await client.delete(f"/api/events/{test_event['id']}/rsvp",
                                            headers={"Authorization": f"Bearer {token}"}
                                            )
            
        assert response2.status_code == 204
        data = response2.json()
        assert data is None

    async def test_rsvp_not_found(self, async_client, test_event, test_user):
        async with async_client as client:
            token = await login_user(client, test_user)
            # Attempt to delete an RSVP that doesn't exist
            response = await client.delete(f"/api/events/{test_event['id']}/rsvp",
                                            headers={"Authorization": f"Bearer {token}"}
                                            )
            
        assert response.status_code == 404
        assert is_error_response(response.json())
        assert error_message_contains(response.json(), "RSVP not found")

    async def test_unauthorized(self, async_client, test_event):
        async with async_client as client:
            response = await client.delete(f"/api/events/{test_event['id']}/rsvp")
            
        assert response.status_code == 401
        assert is_error_response(response.json())
        assert error_message_contains(response.json(), "Not authenticated")
        
    async def test_event_not_found(self, async_client, test_user):
        async with async_client as client:
            token = await login_user(client, test_user)
            response = await client.delete(f"/api/events/9999/rsvp",  # Assuming this ID does not exist
                                            headers={"Authorization": f"Bearer {token}"}
                                            )
            
        assert response.status_code == 404
        assert is_error_response(response.json())
        assert error_message_contains(response.json(), "Event not found")