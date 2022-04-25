from datetime import datetime, timedelta

from pydantic import BaseModel
from pydantic import Field as PydanticField
from sqlmodel import Field, SQLModel

from application.settings import ACCESS_TOKEN_TTL


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(sa_column_kwargs={"unique": True})
    hashed_password: str


class SingInResponse(BaseModel):
    access_token: str
    refresh_token: str


class JWTClaims(BaseModel):
    sub: str
    exp: int = PydanticField(
        default_factory=lambda: int(
            (datetime.now() + timedelta(minutes=ACCESS_TOKEN_TTL)).timestamp()
        )
    )
