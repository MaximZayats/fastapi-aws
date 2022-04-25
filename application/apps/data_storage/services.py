from io import BytesIO
from uuid import uuid4

from botocore.exceptions import ClientError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from types_aiobotocore_s3.service_resource import Bucket

from application.apps.data_storage.exceptions import object_not_found
from application.apps.data_storage.models import UploadInDB


async def get_all_uploads(username: str, db: AsyncSession) -> list[UploadInDB]:
    query = select(UploadInDB).where(UploadInDB.username == username)

    result = await db.execute(query)

    return result.scalars().all()


async def get_file(file_id: str, bucket: Bucket) -> BytesIO:
    b = BytesIO()

    try:
        await bucket.download_fileobj(Key=file_id, Fileobj=b)
    except ClientError:
        raise object_not_found

    return b


def generate_file_id(content_type: str):
    return str(uuid4()) + "-" + content_type.replace("/", "_")


def get_content_type_from_id(uid: str) -> str:
    return uid.split("-")[-1].replace("_", "/")
