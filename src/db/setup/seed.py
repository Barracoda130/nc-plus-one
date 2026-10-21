

import json
from datetime import datetime
from argon2 import PasswordHasher

from src.db.setup.connection import get_connection
from src.db.setup.create_tables import create_all_tables
from src.db.setup.drop_tables import drop_all_tables
from src.db.setup.exceptions import DatabaseError


def parse_data(data: list[dict]) -> list[dict]:
    """
    Parse the data to ready it for inserting into the database. 
    
    - Hashes all fields containing the word "password"
    - Converts all valid fields to a date

    Args:
        data: The data to parse
    """
    ph = PasswordHasher()
    for item in data:
        for key, value in item.items():
            if "password" in key.lower():
                item[key] = ph.hash(value)
            try:
                item[key] = datetime.fromisoformat(value)
            except (ValueError, TypeError):
                pass  # If the value is not a valid date, leave it as is
            
    return data

async def seed_table(table_name: str, data_file: str) -> None:
    """
    Seed database table from the provided file.
    
    Assumes all keys in the file are the same as their respective column names.
    Upon reading an empty file it will return and not raise an error

    Args:
        table_name: Name of the table to seed
        data_file: Path to the JSON file containing the data to seed the table

    Raises:
        DatabaseError: If the data file is empty
    """
    with open(data_file, "r") as file:
        data = json.load(file)

    if len(data) == 0:
        raise DatabaseError(f"No data found in {data_file} to seed {table_name} table")

    data = parse_data(data)
    
    columns = ', '.join(data[0].keys())
    placeholders = ', '.join(f"${i+1}" for i in range(len(data[0])))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"

    async with get_connection() as conn:
        for item in data:
            values = list(item.values())
            await conn.execute(
                query,
                *values
            )


# If every trying to create all these tables they must be created
# in the order these functions are defined because of foreign key constraints.
async def seed_users() -> None:
    await seed_table("users", "db/data/users.json")

async def seed_venues() -> None:
    await seed_table("venues", "db/data/venues.json")
    
async def seed_events() -> None:
    await seed_table("events", "db/data/events.json")
    
async def seed_rsvps() -> None:
    await seed_table("rsvps", "db/data/rsvps.json")
    

async def seed_database() -> None:
    await drop_all_tables()
    await create_all_tables()
    await seed_users()
    await seed_venues()
    await seed_events()
    await seed_rsvps()

