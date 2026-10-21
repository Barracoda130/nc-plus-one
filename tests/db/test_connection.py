

from src.db.connection import get_connection
import pytest


@pytest.mark.asyncio
async def test_get_connection():
    async with get_connection() as conn:
        assert conn is not None