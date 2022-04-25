import aioboto3

from application.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

_session = aioboto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


async def get_s3_bucket():
    async with _session.resource("s3") as s3:
        yield await s3.Bucket("fast-api-service")
