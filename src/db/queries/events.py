

from src.db.connection import get_connection

class EventQueries:
    def __new__(cls):
        raise NotImplementedError("This class should not be instantiated")

    @staticmethod
    async def get_all(order_by: str|None = None) -> list[dict]:
        async with get_connection() as conn:
            if order_by:
                rows = await conn.fetch(f"SELECT * FROM events ORDER BY {order_by};")
            else:
                rows = await conn.fetch("SELECT * FROM events;")
            return [dict(row) for row in rows]