from starlette.config import Config

config = Config(".env")

HOST = config("HOST", cast=str)

DB_URL = config("DB_URL", cast=str)

JWT_SECRET = config("JWT_SECRET", cast=str, default="")
JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str, default="HS256")

ACCESS_TOKEN_TTL = config("ACCESS_TOKEN_TTL", cast=int, default=60)  # minutes
REFRESH_TOKEN_TTL = config("REFRESH_TOKEN_TTL", cast=int, default=43200)  # minutes

AWS_REGION_NAME = config("AWS_REGION_NAME", cast=str)

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", cast=str)
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", cast=str)

SQS_URL = config("SQS_URL", cast=str)
SNS_TOPIC_ARN = config("SNS_TOPIC_ARN", cast=str)
