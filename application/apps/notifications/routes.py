from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from types_aiobotocore_sns import SNSClient

from application.apps.auth.dependencies import get_jtw_claims
from application.apps.auth.models import JWTClaims
from application.apps.data_storage.exceptions import object_not_found
from application.apps.notifications.models import SubscribeRequest
from application.apps.notifications.services import (
    subscribe_user,
    unsubscribe_user,
)

router = APIRouter(tags=["Email notifications"])


@router.post(
    "/subscribe",
    # dependencies=[Depends(get_jtw_claims)],
)
async def subscribe(
    data: SubscribeRequest, db: AsyncSession, sns_client: SNSClient, _: JWTClaims
):
    status = await subscribe_user(email=data.email, db=db, sns_client=sns_client)

    return {"success": status}


@router.delete(
    "/subscribe",
    status_code=202,
    responses={333: {"exception": object_not_found}},
    dependencies=[Depends(get_jtw_claims)],
)
async def unsubscribe(
    data: SubscribeRequest,
    db: AsyncSession = Depends(),
    sns_client: SNSClient = Depends(),
):
    status = await unsubscribe_user(email=data.email, db=db, sns_client=sns_client)

    return {"success": status}
