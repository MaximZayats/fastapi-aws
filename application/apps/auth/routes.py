from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio.session import AsyncSession

from application.apps.auth.exceptions import auth_exception
from application.apps.auth.models import JWTClaims, SingInResponse
from application.apps.auth.services import create_user, get_user_if_exists
from application.apps.auth.utils import generate_jwt

router = APIRouter(tags=["Auth"])


@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def register(username: str, password: str, db: AsyncSession):
    return await create_user(username, password, db)


@router.post("/sign-in", response_model=SingInResponse)
async def login(
    db: AsyncSession,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    if user := await get_user_if_exists(form_data.username, form_data.password, db):
        return SingInResponse(
            access_token=generate_jwt(claims=JWTClaims(sub=user.username)),
            refresh_token="Not implemented",
        )

    raise auth_exception


@router.post("/refresh")
async def refresh(refresh_token: str):
    pass
