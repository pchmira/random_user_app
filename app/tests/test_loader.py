import pytest
from app.user_loader import fetch_users
from aioresponses import aioresponses

@pytest.mark.asyncio
async def test_fetch_users_mocked():
    mocked_data = {
        "results": [
            {
                "gender": "male",
                "name": {"first": "John", "last": "Doe"},
                "phone": "123-456",
                "email": "john.doe@example.com",
                "location": {"city": "New York", "country": "USA"},
                "picture": {"thumbnail": "http://example.com/photo.jpg"}
            }
        ]
    }

    with aioresponses() as mock:
        mock.get("https://randomuser.me/api/?results=1", payload=mocked_data)

        result = await fetch_users(1)
        assert len(result) == 1
        assert result[0]["email"] == "john.doe@example.com"