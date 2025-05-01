from fastapi import HTTPException, WebSocket

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.schema.user.main import ResponseCurrentUser
from src.handlers.token.access_refresh import decode_jwt

import secrets
import string

async def update_key_coin(session: AsyncSession, access_token: str, api_key: str, websocket: WebSocket):
    user_data = ResponseCurrentUser.model_validate(decode_jwt(token=access_token))
    
    user = await session.execute(
        select(User).where(
            and_(
                User.email == user_data.email,
                User.phone_number == user_data.phone_number,
                User.user_name == user_data.user_name
            )
        )
    )
    result = user.scalar_one_or_none()

    if not result:
        await websocket.close(1008, "Пользователь не найден")
        return

    if result.api_key != api_key:
        await websocket.close(1008, "API-KEY не активен")
        return

    if result.req_count >= 100:
        await websocket.close(1008, "Лимит превышен")
        return

    result.req_count += 1
    await session.commit()


async def create_new_api_key(session: AsyncSession, user_data):
    apikey = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(250))

    result = await session.execute(
        select(User).where(
            and_ (
                User.email == user_data.email,
                User.phone_number == user_data.phone_number,
                User.user_name == user_data.user_name
            )
        )
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Пользователь с такими данными не существует")
    user.api_key=apikey
    await session.commit()

    return {"api_key": apikey}


async def delete_api_key(session: AsyncSession, user_data):
    result = await session.execute(
        select(User).where(
            and_ (
                User.email == user_data.email,
                User.phone_number == user_data.phone_number,
                User.user_name == user_data.user_name
            )
        )
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Пользователь с такими данными не существует")

    user.api_key=None

    await session.commit()