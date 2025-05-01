from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    URL_DATABASE: str = "sqlite+aiosqlite:///database.db"

    SECRET_KEY: str = 'few#@^%$f$#@ew#@$few'
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    REFRESH_TOKEN_EXPIRE_DAYS: int = 60 * 24 * 30

settings = Settings()
