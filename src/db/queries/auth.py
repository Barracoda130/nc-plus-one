

from asyncpg import Record

from src.db.connection import get_connection
from src.db.queries.base_query import BaseQuery
from src.db.exceptions import DatabaseError

class AuthQueries(BaseQuery):
    @staticmethod
    async def get_user_by_email(email: str) -> Record|None:
        async with get_connection() as conn:
            user = await conn.fetchrow(
                "SELECT * FROM users WHERE email = $1", email
            )
        return user

    @staticmethod
    async def create_user(user_data: dict) -> Record:
        async with get_connection() as conn:
            user = await conn.fetchrow(
                "INSERT INTO users (name, email, password) VALUES ($1, $2, $3) RETURNING *",
                user_data["name"],
                user_data["email"],
                user_data["password"]
            )
            
        if not user:
            raise DatabaseError("Failed to create user")
        
        return user

    @staticmethod
    async def delete_user_by_id(user_id: int):
        async with get_connection() as conn:
            await conn.execute(
                "DELETE FROM users WHERE id = $1", user_id
            )