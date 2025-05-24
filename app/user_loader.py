import aiohttp
from sqlalchemy.orm import Session
from . import models, schemas, crud

RANDOMUSER_API = "https://randomuser.me/api/"

async def fetch_users(count: int):
    url = f"{RANDOMUSER_API}?results={count}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data["results"]

def transform_user(user_data):
    return schemas.UserCreate(
        gender=user_data["gender"],
        first_name=user_data["name"]["first"],
        last_name=user_data["name"]["last"],
        phone=user_data["phone"],
        email=user_data["email"],
        city=user_data["location"]["city"],
        country=user_data["location"]["country"],
        picture=user_data["picture"]["thumbnail"],
    )

async def load_users(db: Session, count: int):
    users_data = await fetch_users(count)
    for user in users_data:
        user_schema = transform_user(user)
        crud.create_user(db, user_schema)
