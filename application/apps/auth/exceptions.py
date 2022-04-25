from fastapi import HTTPException, status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

auth_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Incorrect username or/and password",
    headers={"WWW-Authenticate": "Bearer"},
)
