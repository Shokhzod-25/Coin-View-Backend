from fastapi import HTTPException

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.schema.user.main import (
    UserRegister, UserLogin,
    ResponseAccessRefreshTokenLogin, ResponseAccessRefreshTokenRegister, ResponseLoginUser,
    ResponseRegisterUser, ResponseCurrentUser
)
from src.models.user import User

from src.handlers.auth.hash_pwd import hash_password, verify_password
from src.handlers.token.access_refresh import create_access_token, create_refresh_token


async def create_user(session: AsyncSession, user_data: UserRegister) -> ResponseAccessRefreshTokenRegister:
    password = hash_password(user_data.password)

    new_user = User(
        user_name=user_data.user_name,
        email=user_data.email,
        phone_number=user_data.phone_number,
        hash_password=password,
        first_name=user_data.first_name
    )
    session.add(new_user)

    await session.commit()
    await session.refresh(new_user)

    data = ResponseRegisterUser.model_validate(new_user)
    access = create_access_token(data=data.model_dump())
    refresh = create_refresh_token(data=data.model_dump())

    return ResponseAccessRefreshTokenRegister(access_token=access, refresh_token=refresh)

async def login_user(session: AsyncSession, user_data: UserLogin, condition) -> ResponseAccessRefreshTokenLogin:
    result = await session.execute(select(User).where(condition))
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.hash_password):
        raise HTTPException(status_code=400, detail="Неверные данные")


    data = ResponseLoginUser.model_validate(user)
    access = create_access_token(data=data.model_dump())
    refresh = create_refresh_token(data=data.model_dump())

    return ResponseAccessRefreshTokenLogin(access_token=access, refresh_token=refresh, api_key=data.api_key)

async def get_current_user(session: AsyncSession, user_data: ResponseCurrentUser) -> ResponseCurrentUser:
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
        raise HTTPException(
            status_code=400,
            detail="Пользователь с такими данными не существует"
        )
    return ResponseCurrentUser.model_validate(user)
