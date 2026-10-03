import pytest
from httpx import AsyncClient, ASGITransport
from main import app
import uuid

@pytest.mark.asyncio
async def test_register(cleanup_test_user):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:

        test_email = f"{uuid.uuid4()}@test.com"
        response = await client.post("/auth/register", json={
            "email": test_email,
            "full_name": "Test User",
            "password": "Test@1234"
        })

        assert response.status_code == 200 
        assert 'id' in response.json()
        assert 'password' not in response.json()

        cleanup_test_user.append(response.json()["id"])

@pytest.mark.asyncio
async def test_login(cleanup_test_user):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        test_email = f"{uuid.uuid4()}@test.com"
        response = await client.post("/auth/register", json={
            "email": test_email,
            "full_name": "Test User",
            "password": "Test@1234"
        })

        assert response.status_code == 200
        cleanup_test_user.append(response.json()["id"])

        login_response = await client.post("/auth/login", data={
            "username": test_email,
            "password": "Test@1234"
        })

        assert login_response.status_code == 200
        assert "access_token" in login_response.json()

@pytest.mark.asyncio
async def test_wrong_password_login(cleanup_test_user):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:

        test_email = f"{uuid.uuid4()}@test.com"

        register_response = await client.post("/auth/register", json={
            "email": test_email,
            "full_name": "Test User",
            "password": "Test@1234"
        })
        
        assert register_response.status_code == 200
        cleanup_test_user.append(register_response.json()["id"])

        response = await client.post("/auth/login",data={
            "username": test_email,
            "password": "Test@123"
        })

        assert response.status_code == 400 








