

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
    return user