

import pytest
from src.db.queries.auth import AuthQueries

@pytest.mark.asyncio
async def test_get_user_by_email_existing_user(test_user):

    user = await AuthQueries.get_user_by_email(test_user["username"])
    assert user is not None
    assert user["email"] == test_user["username"]
    
@pytest.mark.asyncio
async def test_get_user_by_email_non_existing_user():
    user = await AuthQueries.get_user_by_email("asdfasdf")
    assert user is None

@pytest.mark.asyncio
async def test_delete_user_by_id_existing_user(test_user):
    user_id = test_user["id"]
    await AuthQueries.delete_user_by_id(user_id)
    
    # Verify that the user has been deleted
    deleted_user = await AuthQueries.get_user_by_email(test_user["username"])
    assert deleted_user is None
    
@pytest.mark.asyncio
async def test_delete_user_by_id_non_existing_user():
    # Attempt to delete a user with a non-existing ID
    non_existing_user_id = 9999
    await AuthQueries.delete_user_by_id(non_existing_user_id)
    
    # Verify that no exception is raised and the function completes successfully
    assert True

@pytest.mark.asyncio
async def create_user_successful(test_user):
    await AuthQueries.delete_user_by_id(test_user["id"])  # Ensure the user does not exist before creating

    new_user_data = {
        "name": test_user["name"],
        "email": test_user["username"],
        "password": test_user["password"]
    }
    
    user = await AuthQueries.create_user(new_user_data)

    assert user is not None
    assert user["name"] == new_user_data["name"]
    assert user["email"] == new_user_data["email"]
    assert "created_at" in user
    assert "id" in user

    # Test the password is hashed
    assert user["password"] != new_user_data["password"]
