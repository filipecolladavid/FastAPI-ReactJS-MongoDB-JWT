from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from beanie import Document
from src import utils

class Register(BaseModel):
    username: str
    email: str
    password: str


class Login(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str
    email: str
    pic_url: str

# This is the model that will be saved to the database


class User(Document):
    username: str
    email: str
    password: str
    created_at: Optional[datetime] = None
    pic_url: Optional[str] = None
