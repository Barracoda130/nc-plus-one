

from src.db.setup.connection import get_connection

TABLE_NAMES = ["rsvps", "events", "venues", "users"]

async def drop_all_tables() -> None:
    async with get_connection() as conn:
        for table_name in TABLE_NAMES:
            await conn.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")