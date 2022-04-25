from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel


async def save_object(obj: SQLModel, db: AsyncSession):
    db.add(obj)
    await db.commit()
