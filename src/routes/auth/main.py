from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.schema.user.main import UserRegister, UserLogin, ResponseAccessRefreshTokenRegister, ResponseAccessRefreshTokenLogin

from src.models.user import User
from src.handlers.auth.main import create_user, login_user


auth = APIRouter(prefix="/auth", tags=['Auth'])

@auth.post('/register', name="Регистрация", status_code=200, response_model=ResponseAccessRefreshTokenRegister)
async def register(user_data: UserRegister, session: AsyncSession = Depends(get_session)) -> ResponseAccessRefreshTokenRegister:
    user_exists = await session.execute(
        select(User).where(
            or_ (
                User.email == user_data.email,
                User.phone_number == user_data.phone_number,
                User.user_name == user_data.user_name
            )
        )
    )
    user = user_exists.scalar_one_or_none()
    if user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email, номером телефона или именем пользователя уже существует")

    return await create_user(session=session, user_data=user_data)

@auth.post("/login", name="Авторизация", status_code=200, response_model=ResponseAccessRefreshTokenLogin)
async def login_auth_user(user_data: UserLogin, session: AsyncSession = Depends(get_session)) -> ResponseAccessRefreshTokenLogin:
    if user_data.email:
        condition = User.email == user_data.email
    elif user_data.phone_number:
        condition = User.phone_number == user_data.phone_number
    elif user_data.user_name:
        condition = User.user_name == user_data.user_name
    else:
        raise HTTPException(status_code=401, detail="Необходимо указать email, номер телефона или имя пользователя.")

    return await login_user(session=session, user_data=user_data, condition=condition)
