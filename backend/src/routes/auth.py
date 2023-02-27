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

    user_exists = await User.find_one(User.username == credentials.username)
    email_exists = await User.find_one(User.email == credentials.email)
    if user_exists or email_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exists')

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
        pic_url=str(new_user.pic_url)
    )

    return r_user


@router.post('/login')
async def login(credentials: Login, response: Response, Authorize: AuthJWT = Depends()):
    user = await User.find_one(User.username == credentials.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    if not utils.verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect username or password')

    # Create access token

    access_token = Authorize.create_access_token(
        subject=str(user.id),
        expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
    )

    refresh_token = Authorize.create_refresh_token(
        subject=str(user.id),
        expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN)
    )

    # Store refresh and access tokens in cookie
    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token,
                        REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
    
    # Send both access
    return {'status': 'success', 'access_token': access_token}
