import logging

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from application.apps.auth.exceptions import credentials_exception
from application.apps.auth.models import JWTClaims, User
from application.apps.auth.services import get_user
from application.apps.shared.db import get_new_session
from application.settings import JWT_ALGORITHM, JWT_SECRET

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="sign-in")


def get_jtw_claims(token: str = Depends(oauth2_scheme)) -> JWTClaims:
    try:
        return JWTClaims.parse_obj(
            jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM),
        )
    except JWTError as e:
        logging.exception(e)
        raise credentials_exception


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_new_session),
) -> User | None:
    jwt_claims = get_jtw_claims(token)

    user = await get_user(username=jwt_claims.sub, db=db)
    if user is None:
        raise credentials_exception

    return user
