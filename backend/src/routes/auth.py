from datetime import datetime, timedelta
from bson.objectid import ObjectId
from fastapi import APIRouter, Response, status, Depends, HTTPException

from src import oauth2
from ..models.user import User, Login, Register, UserResponse
from .. import utils
from src.oauth2 import AuthJWT
from ..config.settings import settings


router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(credentials: Register):
     
  user_exists = await User.find_one(User.email == credentials.email)
  if user_exists: 
    raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail='Account already exists')
  
  new_user = User(
    username=credentials.username,
    email=credentials.email.lower(),
    password=utils.hash_password(credentials.password),
    created_at=datetime.utcnow()
  )

  await new_user.create()

  r_user = UserResponse(
    username=new_user.username,
    email=new_user.email,
    pic_url= str(new_user.pic_url)
  )

  return r_user

