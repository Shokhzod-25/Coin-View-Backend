from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from starlette.middleware.base import BaseHTTPMiddleware

from src.database import get_session
from src.handlers.token.access_refresh import decode_jwt
from src.models.user import User

class TokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/create-new-api-key", "/token/update-access-token"]:
            authorization = request.headers.get("Authorization")
            if not authorization or not authorization.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Отсутствует или неверный формат токена. Убедитесь, что токен передан правильно.")
            decode_jwt(authorization[7:])
        return await call_next(request)


class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/crypto/get-all"]:
            apikey = request.headers.get("X-API-KEY")
            if not apikey:
                return JSONResponse(status_code=401, content={"detail": "Отсутствует API KEY. Убедитесь, что API KEY передан правильно."})
            async for session in get_session():
                try:
                    result = await session.execute(select(User).where(User.api_key == apikey))
                    user = result.scalar_one_or_none()
                    if not user:
                        return JSONResponse(status_code=401, content={"detail": "Невалидный API-ключ"})
                    user.req_count = (user.req_count or 0) + 1
                    await session.commit()
                except Exception as e:
                    print("Ошибка: ", e)
                    return JSONResponse(status_code=500, content={"detail": "Ошибка сервера при проверке API-ключа"})

        return await call_next(request)

