

from copy import deepcopy
from datetime import datetime
import pytest

from src.db.setup.connection import get_connection
from src.db.setup.create_tables import create_all_tables
from src.db.setup.seed import seed_database, seed_users
from src.db.setup.seed import parse_data


def test_parse_data_hashes_passwords():
    data = [
        {"username": "user1", "password": "password1"},
        {"username": "user2", "password": "password2"}
    ]
    
    parsed_data = parse_data(deepcopy(data))
    
    for original, parsed in zip(data, parsed_data):
        assert original["username"] == parsed["username"]
        assert original["password"] != parsed["password"]  # Password should be hashed
        assert len(parsed["password"]) > 0  # Hashed password should not be empty

def test_parse_data_converts_to_datetime():
    data = [
        {"event_name": "Event 1", "event_date": "2024-01-01T10:00:00"},
        {"event_name": "Event 2", "event_date": "2024-02-01T15:30:00"}
    ]
    
    parsed_data = parse_data(deepcopy(data))
    
    for original, parsed in zip(data, parsed_data):
        assert original["event_name"] == parsed["event_name"]
        assert isinstance(parsed["event_date"], datetime)

def test_parse_data_does_not_change_non_password_non_date_fields():
    data = [
        {"field1": "value1", "field2": 4},
        {"field1": "value3", "field2": 5},
        {"field1": "value5", "field2": 6}
    ]
    
    parsed_data = parse_data(deepcopy(data))
    
    for original, parsed in zip(data, parsed_data):
        assert original["field1"] == parsed["field1"]
        assert original["field2"] == parsed["field2"]

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

    # Remove password hashes as they are salted and will differ even if the rest of the data is identical
    # Remove created_at timestamps as they will differ even if the rest of the data is identical
    omit_keys = ["password", "created_at"]
    database_data1 = [{k: v for k, v in record.items() if k not in omit_keys} for record in database_data1]
    database_data2 = [{k: v for k, v in record.items() if k not in omit_keys} for record in database_data2]
    assert database_data1 == database_data2
    
    
    