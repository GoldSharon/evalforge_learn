from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from auth.models import User

from auth.auth import hash_password

async def create_user(session: AsyncSession, email: str, full_name: str | None , password: str):
    try:
        new_user = User(
            email=email,
            full_name=full_name,
            hashed_password= hash_password(password)
        )
        session.add(new_user)
        await session.commit()
        return new_user

    
    except Exception as e:
        print(f"Error: {e}")
        return None 

async def get_user_by_email(session: AsyncSession, email: str):
    try:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    except Exception as e:
        print(f"Error: {e}")
        return None