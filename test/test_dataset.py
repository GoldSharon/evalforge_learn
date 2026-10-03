import pytest
from httpx import AsyncClient, ASGITransport
from core.database import AsyncSessionLocal

import uuid


from main import app
from auth.models import User 

@pytest.mark.asyncio
async def test_create_dataset(member_token,cleanup_test_dataset):

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:

        create_dataset_response = await client.post(
            "/datasets",
            json = {
                "name": "Deep Learning Dataset",
                "description": "Using for training CNN"
            },
            headers = {
                "Authorization": f"Bearer {member_token}"
            }
        )

        assert create_dataset_response.status_code == 200
        assert "id" in create_dataset_response.json()
        assert "created_at" in create_dataset_response.json()
        assert "description" in create_dataset_response.json()
        cleanup_test_dataset.append(create_dataset_response.json()["id"])




@pytest.mark.asyncio
async def test_delete_dataset_as_member(member_token,cleanup_test_dataset):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:

        create_dataset_response = await client.post(
            "/datasets",
            json={
            "name": "Deep Learning Dataset",
            "description": "User for training CNN"
        },
            headers= {
                "Authorization": f"Bearer {member_token}"
            }
        )

        assert create_dataset_response.status_code == 200 
        assert "id" in create_dataset_response.json()
        assert "created_at" in create_dataset_response.json()
        assert "description" in create_dataset_response.json()

        cleanup_test_dataset.append(create_dataset_response.json()["id"])

        delete_dataset_response = await client.delete(f'''/datasets/{create_dataset_response.json()["id"]}''', 
        headers= {
                    "Authorization": f"Bearer {member_token}"
                }
        )

        assert delete_dataset_response.status_code == 403


@pytest.mark.asyncio
async def test_delete_dataset_as_admin(admin_token,cleanup_test_dataset):

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:

        create_dataset_response = await client.post(
            "/datasets",
            json={
            "name": "Deep Learning Dataset",
            "description": "User for training CNN"
        },
            headers= {
                "Authorization": f"Bearer {admin_token}"
            }
        )

        assert create_dataset_response.status_code == 200 
        assert "id" in create_dataset_response.json()
        assert "created_at" in create_dataset_response.json()
        assert "description" in create_dataset_response.json()

        delete_dataset_response = await client.delete(f'''/datasets/{create_dataset_response.json()["id"]}''', 
        headers= {
                    "Authorization": f"Bearer {admin_token}"
                }
        )
        cleanup_test_dataset.append(create_dataset_response.json()["id"])
        assert delete_dataset_response.status_code == 200



