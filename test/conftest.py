import pytest_asyncio
from sqlalchemy import delete
from database import AsyncSessionLocal
from models import User

@pytest_asyncio.fixture
async def cleanup_test_data():
    yield

    async with AsyncSessionLocal() as session:

        

        await session.execute(
            delete(User).where(User.email == "testuser@test.com")
        )
        await session.commit()