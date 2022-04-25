from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.responses import Response
from types_aiobotocore_s3.service_resource import Bucket
from types_aiobotocore_sqs import SQSClient

from application.apps.auth.models import JWTClaims
from application.apps.data_storage.models import (
    UploadInDB,
    UploadRequest,
    UploadResponse,
)
from application.apps.data_storage.services import (
    generate_file_id,
    get_all_uploads,
    get_content_type_from_id,
    get_file,
)
from application.apps.notifications.services import notify_subscribers
from application.apps.shared.services import save_object

router = APIRouter(tags=["S3 Data"])


@router.get("/get_statistics")
async def get_statistics(  # , response_model=list[UploadInDB]
    claims: JWTClaims,
    db: AsyncSession,
    sqs_client: SQSClient,
):
    # return await sqs_client.receive_message(QueueUrl=SQS_URL)
    return await get_all_uploads(username=claims.sub, db=db)


@router.post("/data")
async def upload_data(
    db: AsyncSession,
    claims: JWTClaims,
    bucket: Bucket,
    sqs_client: SQSClient,
    data: UploadRequest = Depends(),
    do_notify_subscribers: bool = False,
):
    uid = generate_file_id(content_type=data.file.content_type)

    await bucket.put_object(Key=uid, Body=await data.file.read())

    obj = UploadInDB(
        username=claims.sub,
        file_id=uid,
        filename=data.new_filename or data.file.filename,
        content_type=data.file.content_type,
    )

    await save_object(obj, db=db)

    if do_notify_subscribers:
        await notify_subscribers(upload_object=obj, sqs_client=sqs_client)

    return UploadResponse(id=uid)


@router.get("/data/{file_id}")
async def get_data(
    file_id: str,
    bucket: Bucket,
):
    bytes_io = await get_file(file_id=file_id, bucket=bucket)

    response = Response(
        bytes_io.getvalue(),
        media_type=get_content_type_from_id(file_id),
        headers={"Cache-Control": "max-age=604800"},
    )

    return response
