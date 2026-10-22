

import pytest
from src.db.queries.auth import AuthQueries

@pytest.mark.asyncio
async def test_get_user_by_email_existing_user(test_user):

    user = await AuthQueries.get_user_by_email(test_user["username"])
    assert user is not None
    assert user["email"] == test_user["username"]