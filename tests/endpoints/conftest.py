

from fastapi.testclient import TestClient
from pydantic import BaseModel, ValidationError
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

def response_shape(response: dict, expected_shape: type[BaseModel]) -> bool:
    try:
        expected_shape.model_validate(response)
        return True
    except ValidationError:
        return False
