from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from dataset.models import Dataset

async def create_dataset(session: AsyncSession,name: str ,description: str | None):
    try:
        new_dataset = Dataset(name=name, description= description)
        session.add(new_dataset)
        await session.commit()
        return new_dataset

    except Exception as e:
        print(f"Error: {e}")
        return False


async def get_dataset(session: AsyncSession, dataset_id: str):
    try:
        return await session.get(Dataset, dataset_id)  

    except Exception as e:
        print(f"Error: {e}")
        return False

async def delete_dataset(session: AsyncSession, dataset_id: str):
    try:
        result = await get_dataset(session= session, dataset_id=dataset_id)
        if result:
            await session.delete(result)
            print(f"Dataset with id: {dataset_id} is deleted successfully")
            await session.commit()
            return True
        print("No item Found")
        return False   
        

    except Exception as e:
        print(f"Error: {e}")
        return False

async def update_dataset(session: AsyncSession, dataset_id: str , name: str|None, description: str|None):
    try:
        result = await get_dataset(session= session, dataset_id=dataset_id)
        if result:
            if name:
                result.name = name 
                print(f"Name updated to {name} with id {dataset_id}")
            if description:
                result.description = description
                print(f"Name updated with id {dataset_id}")
            await session.commit()
            return result

    except Exception as e:
        print(f"Error: {e}")
        return None






