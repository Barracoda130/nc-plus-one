

from fastapi.testclient import TestClient
import pytest
from httpx import AsyncClient, ASGITransport

from src.app import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def async_client():
    return AsyncClient(transport=ASGITransport(app=app), 
                       base_url="http://test")
