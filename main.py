from fastapi import FastAPI, Depends 

from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from schemas import DatasetCreate, DatasetResponse, DatasetUpdate

from models import User
from dependencies import get_current_user, require_role
from routers import auth
import crud

app = FastAPI()
app.include_router(auth.router)


@app.post("/datasets", response_model=DatasetResponse)
async def create_dataset(
    dataset: DatasetCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return await crud.create_dataset(session, dataset.name, dataset.description)


@app.get("/datasets/{dataset_id}", response_model= DatasetResponse)
async def view_dataset(
    dataset_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return await crud.get_dataset(session, dataset_id=dataset_id)

@app.delete("/datasets/{dataset_id}")
async def delete_dataset(
    dataset_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role("admin"))
):
    result = await crud.delete_dataset(session= session, dataset_id= dataset_id)

    if result:
        return  {"message" : f"Dataset with {dataset_id} deleted"}
    return  {"message" : "Data remianed untouched"}

@app.put("/datasets/{dataset_id}", response_model= DatasetResponse)
async def update_dataset(
    dataset_update: DatasetUpdate,
    dataset_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    result  = await crud.update_dataset(session, dataset_id, dataset_update.name, dataset_update.description)

    if result:
        return result
    else:
        return {"message": "Unable to update dataset"}

