from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from jwt_utils import decode_access_token
from database import get_session
from models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_session)
):
    try:
        payload = decode_access_token(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail= "User id not present")
    

    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail= "User id not found")
    
    return user
    