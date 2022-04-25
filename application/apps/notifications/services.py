from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update
from types_aiobotocore_sns import SNSClient
from types_aiobotocore_sqs import SQSClient

from application.apps.data_storage.models import UploadInDB
from application.apps.notifications.models import SubscribeInDB
from application.settings import HOST, SNS_TOPIC_ARN, SQS_URL


async def subscribe_user(email: str, db: AsyncSession, sns_client: SNSClient) -> bool:
    subscription = await get_subscription(email, db=db)

    if subscription is not None:
        if subscription.is_active:
            return False
        else:
            await db.execute(
                update(SubscribeInDB)
                .where(SubscribeInDB.id == subscription.id)
                .values(is_active=True)
            )

            return True

    response = await sns_client.subscribe(
        TopicArn=SNS_TOPIC_ARN,
        Protocol="Email",
        Endpoint=email,
        ReturnSubscriptionArn=True,
    )

    obj = SubscribeInDB(email=email, subscription_arn=response["SubscriptionArn"])

    db.add(obj)

    try:
        await db.commit()
    except IntegrityError:
        return False

    return True


async def unsubscribe_user(email: str, db: AsyncSession, sns_client: SNSClient) -> bool:
    subscription = await get_subscription(email, db=db)

    if subscription is None:
        return False

    await sns_client.unsubscribe(SubscriptionArn=subscription.subscription_arn)

    return True


async def notify_subscribers(upload_object: UploadInDB, sqs_client: SQSClient) -> None:
    await sqs_client.send_message(
        QueueUrl=SQS_URL,
        MessageBody="New photo: " + upload_object.filename,
        MessageAttributes={
            "url": {
                "DataType": "String",
                "StringValue": "http://" + HOST + "/data/" + upload_object.file_id,
            }
        },
    )


async def get_subscription(email: str, db: AsyncSession) -> SubscribeInDB | None:
    query = select(SubscribeInDB).where(SubscribeInDB.email == email)

    return (await db.execute(query)).scalar()
