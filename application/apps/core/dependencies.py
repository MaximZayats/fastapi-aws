import aioboto3
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from types_aiobotocore_s3.service_resource import Bucket
from types_aiobotocore_sns import SNSClient
from types_aiobotocore_sqs import SQSClient

from application.apps.auth.dependencies import get_jtw_claims
from application.apps.auth.models import JWTClaims
from application.apps.notifications.dependencies import (
    get_sns_client,
    get_sqs_client,
)
from application.apps.shared.db import get_new_session
from application.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def setup_dependencies(app: FastAPI) -> None:
    app.dependency_overrides = {
        **app.dependency_overrides,
        AsyncSession: get_new_session,
        JWTClaims: get_jtw_claims,
        SNSClient: get_sns_client,
        SQSClient: get_sqs_client,
        Bucket: get_s3_bucket,
    }


async def get_s3_bucket():
    session = aioboto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    async with session.resource("s3") as s3:
        yield await s3.Bucket("fast-api-service")
