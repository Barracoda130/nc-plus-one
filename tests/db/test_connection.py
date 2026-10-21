

from src.db.connection import get_connection, _close_connection_pool, _connection_pool, _create_connection_pool
from src.db.exceptions import DatabaseError
from asyncpg import InterfaceError
import pytest


@pytest.mark.asyncio
async def test_get_connection():
    async with get_connection() as conn:
        assert conn is not None

@pytest.mark.asyncio
async def test_get_connection_used_outside_context_manager():
    conn = get_connection()
    with pytest.raises(DatabaseError):
        await conn.fetch("SELECT 1;")  # Attempt to use the connection outside of the context manager

@pytest.mark.asyncio
async def test_get_connection_released_after_context_manager():
    async with get_connection() as conn:
        assert conn is not None

    with pytest.raises(InterfaceError):
        await conn.fetch("SELECT 1;")  # Attempt to use the connection after it has been released

@pytest.mark.asyncio
async def test_get_connection_multiple_times():
    async with get_connection() as conn1:
        assert conn1 is not None
        async with get_connection() as conn2:
            assert conn2 is not None
            assert conn1 != conn2
            

        
    