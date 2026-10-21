

import pytest

from src.db.connection import get_connection
from src.db.create_tables import create_all_tables
from src.db.seed import seed_database, seed_users


@pytest.mark.asyncio
async def test_seed_database_creates_tables_and_seeds_users():
    print("0")
    await seed_database()
    
    print("1")
    async with get_connection() as conn:
        tables = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")

    print("2")
    tables = [table[0] for table in tables]

    assert "users" in tables
    assert "venues" in tables
    assert "events" in tables
    assert "rsvps" in tables

    async with get_connection() as conn:
        user_count = await conn.fetchval("SELECT COUNT(*) FROM users;")

    assert user_count
    assert user_count > 0
    
@pytest.mark.asyncio
async def test_seed_database_produces_identical_state():
    await seed_database()
    
    async with get_connection() as conn:
        database_data1 = await conn.fetch("SELECT * FROM users, venues, events, rsvps;")
    
    await seed_database()
    
    async with get_connection() as conn:
        database_data2 = await conn.fetch("SELECT * FROM users, venues, events, rsvps;")

    assert database_data1 == database_data2
    
    
    