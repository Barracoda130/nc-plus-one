

import pytest

from src.db.queries.auth import AuthQueries


@pytest.mark.asyncio
async def test_login_valid_user(async_client, test_user):
    async with async_client as client:
        body = {
            "username": test_user["username"],
            "password": test_user["password"]
        }
        response = await client.post("/api/auth/login", data=body)
        
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_user(async_client):
    async with async_client as client:
        body = {
            "username": "invaliduser",
            "password": "invalidpassword"
        }
        response = await client.post("/api/auth/login", data=body)
        
    assert response.status_code == 401
    
@pytest.mark.asyncio
async def test_register_user(async_client, test_user):
    await AuthQueries.delete_user_by_id(test_user["id"])  # Ensure the user does not exist before registering
    
    async with async_client as client:
        body = {
            "name": "name",
            "email": test_user["username"],
            "password": test_user["password"]
        }
        response = await client.post("/api/auth/register", json=body)

    assert response.status_code == 201
    user_data = response.json()["user"]
    assert "id" in user_data
    assert user_data["name"] == "name"
    assert user_data["email"] == test_user["username"]
    
@pytest.mark.asyncio
async def test_register_existing_user(async_client, test_user):
    async with async_client as client:
        body = {
            "name": "name",
            "email": test_user["username"],
            "password": test_user["password"]
        }
        response = await client.post("/api/auth/register", json=body)
    
    print(f"Response status code: {response.status_code}, Response body: {response.json()}")  # Debugging line

    assert response.status_code == 409
    assert response.json()["detail"]["error"]["message"]== "User with this email already exists"