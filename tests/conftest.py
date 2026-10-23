

from datetime import datetime
import os
from unittest.mock import AsyncMock, MagicMock
from argon2 import PasswordHasher
from asyncpg import UniqueViolationError
import pytest_asyncio
import pytest
from src.db.connection import _close_connection_pool, get_connection
from src.db.setup.drop_tables import drop_all_tables
from src.db.setup.seed import seed_database

def pytest_configure():
    """
    Configure pytest to use the 'nc_plus_one_test' database for testing.
    """
    os.environ["DATABASE_NAME"] = "nc_plus_one_test"

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    
    await seed_database()
    
    yield  # Run the tests
    
    await drop_all_tables()
    await _close_connection_pool()

    
class EmptyDatabaseConnectionManager:
    """
    A fake connection manager used to simulate an empty database.
    """

    def __init__(self):
        self.connection = MagicMock()
        self.connection.fetch = AsyncMock(return_value=[])  
        self.connection.fetchrow = AsyncMock(return_value=None)
        self.connection.execute = AsyncMock(return_value=None)
        
    async def __aenter__(self):
        return self.connection
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    
@pytest.fixture
def empty_database(monkeypatch: pytest.MonkeyPatch):
    """
    Fixture to simulate an empty database by monkeypatching the get_connection function.
    """
    def patch_lookup_location(lookup_location: str) -> EmptyDatabaseConnectionManager:
        manager = EmptyDatabaseConnectionManager()
        monkeypatch.setattr(lookup_location, lambda: manager)
        return manager
    yield patch_lookup_location

    
@pytest.fixture
async def test_user():
    user = {
        "username": "testuser",
        "password": "testpassword"
    }
    ph = PasswordHasher()
    hashed_password = ph.hash(user["password"])
    async with get_connection() as conn:
        try:
            await conn.execute(
                "INSERT INTO users (email, password, name) VALUES ($1, $2, $3) RETURNING id",
                user["username"], 
                hashed_password,
                "test name"
            )
        except UniqueViolationError:
            pass  # User already exists, ignore the error

        user_id = await conn.fetchval("SELECT id FROM users WHERE email = $1", "testuser",)
        
    assert user_id
    user["id"] = user_id
    yield user
    
    # Clean up the test user
    async with get_connection() as conn:
        await conn.execute("DELETE FROM users WHERE id = $1", user_id)

async def login_user(client, user):
    response = await client.post("/api/auth/login", 
                           data={"username": user["username"], 
                                 "password": user["password"]})
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    return token

@pytest.fixture
async def test_event():
    event = {
        "title": "Test Event",
        "description": "This is a test event.",
        "starts_at": datetime.fromisoformat("2024-01-01T10:00:00Z"),
        "ends_at": datetime.fromisoformat("2024-01-01T12:00:00Z")
    }

    async with get_connection() as conn:
        event_id = await conn.fetchval(
            "INSERT INTO events (title, description, starts_at, ends_at) VALUES ($1, $2, $3, $4) RETURNING id",
            event["title"], event["description"], event["starts_at"], event["ends_at"]
        )

    assert event_id
    event["id"] = event_id
    yield event
    
    # Clean up the test event
    async with get_connection() as conn:
        await conn.execute("DELETE FROM events WHERE id = $1", event_id)

def error_message_contains(response: dict|None, expected_message: str) -> bool:
    if not response:
        return False
    
    message = response["detail"]["error"]["message"]
    if not message:
        return False
    
    return expected_message in str(message)

def is_error_response(response: dict|None) -> bool:
    if not response:
        return False
    
    return ("error" in response["detail"] and
            "message" in response["detail"]["error"] and
            "code" in response["detail"]["error"])
