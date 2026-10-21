

import pytest

from src.db.connection import get_connection
from src.db.setup.create_tables import create_all_tables
from src.db.setup.drop_tables import drop_all_tables




@pytest.mark.asyncio
async def test_create_all_tables():
    
    await drop_all_tables() 

    await create_all_tables()
    
    async with get_connection() as conn:
        tables = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")

    tables = [table[0] for table in tables]

    assert "users" in tables
    assert "venues" in tables
    assert "events" in tables
    assert "rsvps" in tables

    
@pytest.mark.asyncio
async def test_create_all_tables_already_exist():
    print("1")
    await create_all_tables()  # Create tables for the first time
    print("2")
    await create_all_tables()  # Attempt to create tables again
    print("3")
    
    async with get_connection() as conn:
        tables = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")

    tables = [table[0] for table in tables]

    assert "users" in tables
    assert "venues" in tables
    assert "events" in tables
    assert "rsvps" in tables
    
    