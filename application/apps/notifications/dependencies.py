from typing import AsyncGenerator

import aioboto3
from types_aiobotocore_sns import SNSClient
from types_aiobotocore_sqs import SQSClient

from application.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_REGION_NAME,
    AWS_SECRET_ACCESS_KEY,
)

_session = aioboto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME,
)


async def get_sns_client() -> AsyncGenerator[SNSClient, None]:
    async with _session.client("sns") as sns:
        yield sns


async def get_sqs_client() -> AsyncGenerator[SQSClient, None]:
    async with _session.client("sqs") as sqs:
        yield sqs
