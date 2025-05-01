from fastapi import Header, APIRouter
from typing import Annotated
from ...handlers.token.access_refresh import create_access_token, decode_jwt

token = APIRouter(prefix='/token', tags=['Token'])

@token.get("/update-access-token")
async def update_access_token(
        authorization: Annotated[str | None, Header()] = None,
):
    return {"access_token": create_access_token(decode_jwt(authorization[7:]))}
