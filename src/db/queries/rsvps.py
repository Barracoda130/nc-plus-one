

from asyncpg import Record

from src.db.connection import get_connection
from src.db.queries.base_query import BaseQuery
from src.db.setup.exceptions import DatabaseError


class RSVPQueries(BaseQuery):
    @classmethod
    async def create_rsvp(cls, event_id: int, user_id: int) -> Record:
        # Check if the RSVP already exists
        async with get_connection() as conn:
            existing_rsvp = await conn.fetchrow(
                "SELECT * FROM rsvps WHERE event_id = $1 AND attendee_id = $2",
                event_id,
                user_id,
            )
            if existing_rsvp:
                raise DatabaseError("RSVP already exists")
            
            rsvp = await conn.fetchrow(
                "INSERT INTO rsvps (event_id, attendee_id) VALUES ($1, $2) RETURNING *",
                event_id,
                user_id,
            )
            
            if not rsvp:
                raise DatabaseError("Failed to create RSVP")
            
            return rsvp
    