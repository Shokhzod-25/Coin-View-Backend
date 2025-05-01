from typing import Annotated

from fastapi import APIRouter, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.handlers.auth.main import get_current_user
from src.handlers.token.access_refresh import decode_jwt
from src.schema.user.main import ResponseCurrentUser

user = APIRouter(prefix="/user")

@user.get("/current-user", response_model=ResponseCurrentUser)
async def current_user(
        authorization: Annotated[str | None, Header()] = None,
        session: AsyncSession = Depends(get_session)
) -> ResponseCurrentUser:
    decode_jwt_token = decode_jwt(token=authorization[7:])
    user_data = ResponseCurrentUser.model_validate(decode_jwt_token)
    result = await get_current_user(session=session, user_data=user_data)
    return result
