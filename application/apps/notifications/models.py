from datetime import datetime

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel


class SubscribeRequest(BaseModel):
    email: EmailStr


class UnSubscribeRequest(BaseModel):
    email: EmailStr


class SubscribeInDB(SQLModel, table=True):
    __tablename__ = "subscriber"

    id: int = Field(primary_key=True)
    email: str = Field(sa_column_kwargs={"unique": True})
    subscription_timestamp: datetime = Field(default_factory=lambda: datetime.now())
    subscription_arn: str
    is_active: bool = True
