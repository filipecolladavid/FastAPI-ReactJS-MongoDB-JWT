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


# Register new User - to be removed if webapp is private
@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(credentials: Register):

    if not utils.is_valid_email(credentials.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid email'
        )

    user_exists = await User.find_one(User.username == credentials.username)
    email_exists = await User.find_one(User.email == credentials.email)
    if user_exists or email_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Account already exists'
        )

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


# Sign In user
@router.post('/login')
async def login(credentials: Login, response: Response, Authorize: AuthJWT = Depends()):
    user = await User.find_one(User.username == credentials.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    if not utils.verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect username or password'
        )

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


# Refresh Acess Token
@router.get('/refresh')
async def refresh_token(response: Response, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not refresh access token'
            )

        user = await User.get(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='The user belonging to this token no logger exist'
            )
        access_token = Authorize.create_access_token(
            subject=str(user.id),
            expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
        )
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Please provide refresh token'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )

    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    return {'access_token': access_token}


# Logout user
@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, Authorize: AuthJWT = Depends(), user_id: str = Depends(oauth2.require_user)):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)

    return {'status': 'success'}
