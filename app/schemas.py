from pydantic import BaseModel

class UserBase(BaseModel):
    gender: str
    first_name: str
    last_name: str
    phone: str
    email: str
    city: str
    country: str
    picture: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
