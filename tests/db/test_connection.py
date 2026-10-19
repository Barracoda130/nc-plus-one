

from src.db.connection import get_connection
import pytest

@pytest.fixture
def conn():
    connection = get_connection()
    yield connection
    connection.close()

def test_get_connection(conn):
    assert conn is not None