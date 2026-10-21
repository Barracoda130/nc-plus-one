

import pytest

from src.db.connection import get_connection
from src.db.drop_tables import drop_all_tables

@pytest.mark.asyncio
async def test_drop_all_tables():
    
    async with get_connection() as conn:
    # Create tables first
        await conn.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY);")
        await conn.execute("CREATE TABLE IF NOT EXISTS venues (id SERIAL PRIMARY KEY);")
        await conn.execute("CREATE TABLE IF NOT EXISTS events (id SERIAL PRIMARY KEY);")
        await conn.execute("CREATE TABLE IF NOT EXISTS rsvps (id SERIAL PRIMARY KEY);")
    
    # Now drop all tables
    await drop_all_tables()

    async with get_connection() as conn:
        # Check if tables are dropped
        tables = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")

    tables = [table[0] for table in tables]

    assert "users" not in tables
    assert "venues" not in tables
    assert "events" not in tables
    assert "rsvps" not in tables

@pytest.mark.asyncio
async def test_drop_all_tables_when_no_tables_exist():
    await drop_all_tables()  # Attempt to drop tables when none exist
    await drop_all_tables()  # Attempt to drop tables again to ensure no errors occur
    
    