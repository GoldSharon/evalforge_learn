import uuid

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from auth.models import User
from core.database import DATABASE_URL, get_session
from dataset.models import Dataset
from main import app


test_engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_session():
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="session", autouse=True)
async def configure_test_app():
    app.dependency_overrides[get_session] = override_get_session
    yield
    app.dependency_overrides.pop(get_session, None)
    await test_engine.dispose()


@pytest_asyncio.fixture
async def cleanup_test_user():
    user_ids = []
    yield user_ids

    if user_ids:
        async with TestSessionLocal() as session:
            await session.execute(delete(User).where(User.id.in_(user_ids)))
            await session.commit()


@pytest_asyncio.fixture
async def cleanup_test_dataset():
    dataset_ids = []
    yield dataset_ids

    if dataset_ids:
        async with TestSessionLocal() as session:
            await session.execute(delete(Dataset).where(Dataset.id.in_(dataset_ids)))
            await session.commit()


@pytest_asyncio.fixture
async def admin_token():
    test_email = f"{uuid.uuid4()}@test.com"
    test_user_password = "Test@1234"

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        register_response = await client.post(
            "/auth/register",
            json={
                "email": test_email,
                "full_name": "Test User",
                "password": test_user_password,
            },
        )

        assert register_response.status_code == 200
        user_id = register_response.json()["id"]

        try:
            async with TestSessionLocal() as session:
                test_user = await session.get(User, user_id)
                assert test_user is not None
                test_user.role = "admin"
                await session.commit()

            login_response = await client.post(
                "/auth/login",
                data={
                    "username": test_email,
                    "password": test_user_password,
                },
            )

            assert login_response.status_code == 200
            yield login_response.json()["access_token"]
        finally:
            async with TestSessionLocal() as session:
                await session.execute(delete(User).where(User.id == user_id))
                await session.commit()


@pytest_asyncio.fixture
async def member_token():
    test_email = f"{uuid.uuid4()}@test.com"
    test_user_password = "Test@1234"

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        register_response = await client.post(
            "/auth/register",
            json={
                "email": test_email,
                "full_name": "Test User",
                "password": test_user_password,
            },
        )

        assert register_response.status_code == 200
        user_id = register_response.json()["id"]

        try:
            login_response = await client.post(
                "/auth/login",
                data={
                    "username": test_email,
                    "password": test_user_password,
                },
            )

            assert login_response.status_code == 200
            yield login_response.json()["access_token"]
        finally:
            async with TestSessionLocal() as session:
                await session.execute(delete(User).where(User.id == user_id))
                await session.commit()
