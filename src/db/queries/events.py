

from src.db.connection import get_connection
from src.db.queries.base_query import BaseQuery

class EventQueries(BaseQuery):
    @staticmethod
    async def get_all(order_by: str|None = None) -> list[dict]:
        async with get_connection() as conn:
            if order_by:
                rows = await conn.fetch(f"SELECT * FROM events ORDER BY {order_by};")
            else:
                rows = await conn.fetch("SELECT * FROM events;")
            return [dict(row) for row in rows]

    @staticmethod
    async def get_by_id(event_id: int) -> dict|None:
        async with get_connection() as conn:
            row = await conn.fetchrow("SELECT * FROM events WHERE id = $1;", event_id)
            return dict(row) if row else None