from typing import Annotated

from fastapi import APIRouter, Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.handlers.api_key.main import create_new_api_key as create_api_key, delete_api_key as delete_apikey
from src.handlers.token.access_refresh import decode_jwt
from src.schema.user.main import ResponseCurrentUser

api_key = APIRouter(prefix="/api-key", tags=['API KEY'])

@api_key.get('/create-new-api-key')
async def create_new_api_key(
        authorization: Annotated[str | None, Header()] = None,
        session: AsyncSession = Depends(get_session)
):
    decode_jwt_token = decode_jwt(token=authorization[7:])
    user_data = ResponseCurrentUser.model_validate(decode_jwt_token)

    return await create_api_key(session=session, user_data=user_data)


@api_key.delete('/delete-api-key')
async def delete_api_key(
        authorization: Annotated[str | None, Header()] = None,
        session: AsyncSession = Depends(get_session)
):
    decode_jwt_token = decode_jwt(token=authorization[7:])
    user_data = ResponseCurrentUser.model_validate(decode_jwt_token)
    await delete_apikey(session=session, user_data=user_data)

    return {"message": "ok"}

