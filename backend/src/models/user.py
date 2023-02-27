from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from beanie import Document, Indexed

class Register(BaseModel):
    username: str
    email: EmailStr
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
    created_at: Optional[datetime] =  None         
    pic_url: Optional[str] = None