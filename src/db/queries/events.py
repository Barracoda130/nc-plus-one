

from src.db.connection import get_connection

class EventQueries:
    def __new__(cls):
        raise NotImplementedError("This class should not be instantiated")

    @staticmethod
    async def get_all() -> list[dict]:
        async with get_connection() as conn:
            rows = await conn.fetch("SELECT * FROM events;")
            return [dict(row) for row in rows]