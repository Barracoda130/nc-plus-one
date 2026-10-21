

import json
from argon2 import PasswordHasher

from src.db.connection import get_connection
from src.db.create_tables import create_all_tables
from src.db.drop_tables import drop_all_tables




async def seed_users():
    ph = PasswordHasher()

    # Insert from db/data/users.json
    with open("db/data/users.json", "r") as file:
        users_data = json.load(file)

        async with get_connection() as conn:
            for user in users_data:
                await conn.execute(
                    "INSERT INTO users (name, email, password) VALUES ($1, $2, $3);",
                    user["name"], user["email"], ph.hash(user["password"])
                )
            

    

async def seed_database():
    await drop_all_tables()
    await create_all_tables()
    await seed_users()