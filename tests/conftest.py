

import pytest_asyncio
from src.db.setup.connection import _close_connection_pool

@pytest_asyncio.fixture(autouse=True)
async def close_connection_pool_after_tests():
    yield
    await _close_connection_pool()