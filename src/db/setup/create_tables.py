

import asyncpg

from src.db.setup.connection import get_connection

SCHEMA_FILE = "db/schema.sql"


async def create_all_tables() -> None:
    with open(SCHEMA_FILE, "r") as file:
        schema_sql = file.read()

    async with get_connection() as conn:
        await conn.execute(schema_sql)
