

import os
import pytest_asyncio
import pytest
from src.db.connection import _close_connection_pool
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
    await _close_connection_pool()  # Close the connection pool after seeding to ensure a clean state for tests
    
    yield  # Run the tests
    
    await drop_all_tables()
    await _close_connection_pool()

@pytest_asyncio.fixture(autouse=True)
async def close_connection_pool_after_tests():
    yield
    await _close_connection_pool()