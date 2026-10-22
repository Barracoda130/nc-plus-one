

import pytest


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