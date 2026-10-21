

from typing import Any

import asyncpg
import os
from dotenv import load_dotenv
from src.db.setup.exceptions import DatabaseError

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
    """
    Gets a connection from the connection pool.
    
    If the pool does not exist it will create a new pool
    and then get a connection from that pool

    Raises:
        DatabaseError: Raised if the result from Pool.aquire() is not a Connection

    Returns:
        A connection to the database from the pool
    """
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
    """
    Forces the user to use asyncpg.Connection within a context manager
    to ensure that the connection gets released when it is no longer being used.
    """
    def __init__(self):
        self.conn: asyncpg.Connection|None = None

    async def __aenter__(self) -> asyncpg.Connection:
        self.conn = await _get_connection_asyncpg()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.conn is not None:
            await _release_connection(self.conn)
            self.conn = None

    def __getattr__(self, name: str) -> Any:
        if name in dir(asyncpg.Connection):
            raise DatabaseError("Connection can only be used within the context manager")
        
        return super().__getattribute__(name)

def get_connection() -> ConnectionManager:
    return ConnectionManager()

    



    