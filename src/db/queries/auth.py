

from asyncpg import Record

from src.db.connection import get_connection
from src.db.queries.base_query import BaseQuery

class AuthQueries(BaseQuery):
    @staticmethod
    async def get_user_by_email(email: str) -> Record|None:
        async with get_connection() as conn:
            user = await conn.fetchrow(
                "SELECT * FROM users WHERE email = $1", email
            )
        return user