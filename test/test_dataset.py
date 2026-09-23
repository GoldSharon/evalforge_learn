import pytest
from httpx import AsyncClient, ASGITransport
from main import app



@pytest.mark.asyncio
async def test_create_dataset(clean_test_user,clean_test_dataset):

    async with ASGITransport(transport=AsyncClient(app=app), base_url="http://test") as client:

        register_response = await client.post("/auth/register", json={
            "email": "testuser@test.com",
            "full_name": "Test User",
            "password": "Test@1234"
        })

        assert register_response.status_code == 200

        login_response = await client.post("/auth/login", data={
            "username": "testuser@test.com",
            "password": "Test@1234"
        })

        assert login_response.status_code == 200

        create_dataset_response = await client.post(
            "/datasets",
            json = {
                "name": "Deep Learning Dataset",
                "description": "Using for training CNN"
            },
            headers = {
                "Authorization": f"Bearer {login_response.json()["access_token"]}"
            }
        )

        assert create_dataset_response.status_code = 200
        assert "id" in create_dataset_response.json()
        assert "created_at" in create_dataset_response.json()
        assert "description" in create_dataset_response.json()


@pytest.mark.asyncio
async def test_delete_dataset_as_member(cleanup_test_user):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:

        register_response = await client.post("/auth/register", json={
            "email": "testuser@test.com",
            "full_name": "Test User",
            "password": "Test@1234"
        })

        assert register_response.status_code == 200

        login_response = await client.post("/auth/login", data={
            "username": "testuser@test.com",
            "password": "Test@1234"
        })

        assert login_response.status_code == 200


        create_dataset_response = await client.post(
            "/datasets",
            json={
            "name": "Deep Learning Dataset",
            "description": "User for training CNN"
        },
            headers= {
                "Authorization": f"Bearer {login_response.json()["access_token"]}"
            }
        )

        assert create_dataset_response.status_code == 200 
        assert "id" in create_dataset_response.json()
        assert "created_at" in create_dataset_response.json()
        assert "description" in create_dataset_response.json()

        delete_dataset_response = await client.delete(f'''/datasets/{create_dataset_response.json()["id"]}''', 
        headers= {
                    "Authorization": f"Bearer {login_response.json()["access_token"]}"
                }
        )


        assert delete_dataset_response.status_code == 403


@pytest.mark.asyncio
async def test_delete_dataset_as_admin(cleanup_test_user):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:


        login_response = await client.post("/auth/login", data={
            "username": "GoldSharonR@hexaware.com",
            "password": "Admin@1234"
        })

        assert login_response.status_code == 200


        create_dataset_response = await client.post(
            "/datasets",
            json={
            "name": "Deep Learning Dataset",
            "description": "User for training CNN"
        },
            headers= {
                "Authorization": f"Bearer {login_response.json()["access_token"]}"
            }
        )

        assert create_dataset_response.status_code == 200 
        assert "id" in create_dataset_response.json()
        assert "created_at" in create_dataset_response.json()
        assert "description" in create_dataset_response.json()

        delete_dataset_response = await client.delete(f'''/datasets/{create_dataset_response.json()["id"]}''', 
        headers= {
                    "Authorization": f"Bearer {login_response.json()["access_token"]}"
                }
        )


        assert delete_dataset_response.status_code == 200