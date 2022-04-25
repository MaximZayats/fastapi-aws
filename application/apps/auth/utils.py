from jose import jwt
from passlib.context import CryptContext

from application.apps.auth.models import JWTClaims
from application.settings import JWT_ALGORITHM, JWT_SECRET

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, hashed_password: str, salt: str = "") -> bool:
    return pwd_context.verify(password + salt, hashed_password)


def get_password_hash(password: str, salt: str = "") -> str:
    return pwd_context.hash(password + salt)


def generate_jwt(claims: JWTClaims, secret_key: str = JWT_SECRET) -> str:
    return jwt.encode(
        claims=claims.dict(),
        algorithm=JWT_ALGORITHM,
        key=secret_key,
    )


def generate_refresh_token() -> str:
    pass
