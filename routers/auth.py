from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from schemas import UserCreate, UserResponse
from crud import create_user,get_user_by_email
from auth import verify_password
from jwt_utils import create_access_token

router = APIRouter(prefix= "/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):

    result = await get_user_by_email(session, user.email)

    if not result:
        return await create_user(session, user.email, user.full_name, user.password)

    else:
        raise HTTPException(status_code=400, detail="Email already registered")

@router.post("/login")
async def login(email: str, password: str, session: AsyncSession = Depends(get_session)):

    result = await get_user_by_email(session, email)

    if result:
        if verify_password(password, result.hashed_password):
            token = create_access_token(data={"sub": result.id})
            return {"access_token": token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=400, detail="User password is incorrect")
    else:
        raise HTTPException(status_code=400, detail="User is not registered")
    
        


        
