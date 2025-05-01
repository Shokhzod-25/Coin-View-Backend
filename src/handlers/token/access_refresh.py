from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import jwt
from fastapi import HTTPException

from src.config import settings

ALGORITHM: str = settings.ALGORITHM
SECRET_KEY: str = settings.SECRET_KEY

def create_token(data: Dict[str, Any], expr: int) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expr)
    to_encode["exp"] = expire.timestamp()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(data: Dict[str, Any]) -> str:
    return create_token(data, settings.ACCESS_TOKEN_EXPIRE_MINUTES)

def create_refresh_token(data: Dict[str, Any]) -> str:
    return create_token(data, settings.REFRESH_TOKEN_EXPIRE_DAYS)


def decode_jwt(token: str) -> Optional[Dict[str, Any]]:
    try:
        result = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if result:
            return result
        raise HTTPException(status_code=401, detail="Невалидный или просроченный токен")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Токен просрочен. Пожалуйста, обновите токен.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Неизвестная ошибка: {str(e)}. Пожалуйста, попробуйте позже.")
