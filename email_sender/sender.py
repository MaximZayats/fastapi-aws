import asyncio
from asyncio import sleep
from os import getenv

import aioboto3
import requests
from dotenv import load_dotenv
from types_aiobotocore_sqs import SQSClient
from types_aiobotocore_sqs.type_defs import MessageTypeDef

load_dotenv()

TG_TOKEN = getenv("TG_TOKEN")
QUEUE_URL = getenv("SQS_URL")
WAIT_TIME_SECONDS = 10

_session = aioboto3.Session(
    aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=getenv("AWS_REGION_NAME"),
)

_sqs_client = _session.client("sqs")
_sns_client = _session.client("sns")


async def notify(messages: list[MessageTypeDef]) -> None:
    message_text = "New posts!\n"

    for idx, message in enumerate(messages, 1):
        url = message["MessageAttributes"]["url"]["StringValue"]
        message_text += f'<a href="{url}">{idx}. Watch on the website</a>\n'

    requests.get(
        f"http://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        params={"chat_id": 630665299, "text": message_text, "parse_mode": "html"},
    )


async def main():
    async with _sqs_client as sqs:  # type: SQSClient
        while True:
            response = await sqs.receive_message(
                QueueUrl=QUEUE_URL,
                MessageAttributeNames=("url",),
                MaxNumberOfMessages=10,
                WaitTimeSeconds=WAIT_TIME_SECONDS,
            )

            if "Messages" not in response:
                continue

            await notify(response["Messages"])

            for message in response["Messages"]:
                await sqs.delete_message(
                    QueueUrl=QUEUE_URL, ReceiptHandle=message["ReceiptHandle"]
                )

            await sleep(WAIT_TIME_SECONDS)


if __name__ == "__main__":
    asyncio.run(main())
