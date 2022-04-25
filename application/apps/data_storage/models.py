from fastapi import UploadFile
from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class UploadRequest(BaseModel):
    file: UploadFile
    new_filename: str | None = None


class UploadResponse(BaseModel):
    id: str


class UploadInDB(SQLModel, table=True):
    __tablename__ = "upload"

    id: int = Field(primary_key=True)
    username: str
    file_id: str
    filename: str
    content_type: str
