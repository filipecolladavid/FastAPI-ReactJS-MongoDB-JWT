from fastapi import APIRouter, Depends

from ..models.user import User, UserResponse
from .. import oauth2

router = APIRouter()


@router.get('/me', response_model=UserResponse)
async def get_me(user_id: str = Depends(oauth2.require_user)):
    
    user = await User.get(str(user_id))
    r_user = UserResponse(
        username=user.username,
        email=user.email,
        pic_url=str(user.pic_url)
    )
    return r_user
