

import asyncpg
import os
from dotenv import load_dotenv
from src.db.exceptions import DatabaseError

load_dotenv(".env")

_connection_pool: asyncpg.pool.Pool|None = None

async def _create_connection_pool() -> asyncpg.pool.Pool:
    database_name = os.environ.get("DATABASE_NAME")
    database_user = os.environ.get("DATABASE_USER")
    database_password = os.environ.get("DATABASE_PASSWORD")
    
    pool = await asyncpg.create_pool(
        user=database_user,
        password=database_password,
        database=database_name,
        host="localhost"
    )
    if not pool:
        raise DatabaseError("Failed to create connection pool")
    return pool

async def _release_connection(conn: asyncpg.Connection) -> None:
    global _connection_pool
    if _connection_pool is not None and conn is not None:
        await _connection_pool.release(conn)

async def _get_connection_asyncpg() -> asyncpg.Connection:
    global _connection_pool
    if _connection_pool is None:
        _connection_pool = await _create_connection_pool()
    
    conn = await _connection_pool.acquire()
    if not isinstance(conn, asyncpg.Connection):
        raise DatabaseError("Failed to acquire a connection from the pool")
    return conn

async def _close_connection_pool() -> None:
    global _connection_pool
    if _connection_pool is not None:
        await _connection_pool.close()
        _connection_pool = None

class ConnectionManager:
    def __init__(self):
        self.conn: asyncpg.Connection|None = None

    async def __aenter__(self) -> asyncpg.Connection:
        self.conn = await _get_connection_asyncpg()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.conn is not None:
            await _release_connection(self.conn)
            self.conn = None

def get_connection() -> ConnectionManager:
    return ConnectionManager()

    



    