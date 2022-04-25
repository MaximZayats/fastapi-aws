from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from application.settings import DB_URL

_engine = create_async_engine(DB_URL, echo=True, future=True)
_async_session_maker = sessionmaker(
    _engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    async with _engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_new_session() -> AsyncGenerator[AsyncSession, None]:
    async with _async_session_maker() as session:
        yield session
