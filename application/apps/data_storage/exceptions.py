from fastapi import HTTPException
from starlette import status

object_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Object not found",
    headers={"WWW-Authenticate": "Bearer"},
)
