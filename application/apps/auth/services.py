from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from application.apps.auth.models import User
from application.apps.auth.utils import get_password_hash, verify_password


async def create_user(username: str, password: str, db: AsyncSession) -> User | None:
    user = User(
        username=username,
        hashed_password=get_password_hash(password, salt=username),
    )

    try:
        db.add(user)
        await db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="user already registered",
        )

    return user


async def get_user(db: AsyncSession, **kwargs) -> User | None:
    users = await db.execute(select(User).filter_by(**kwargs))

    # user_row = users.scalars().first()

    return users.scalar()


async def get_user_if_exists(
    username: str, password: str, db: AsyncSession
) -> User | None:
    user = await get_user(username=username, db=db)

    if user and verify_password(password, user.hashed_password, salt=user.username):
        return user

    return None
