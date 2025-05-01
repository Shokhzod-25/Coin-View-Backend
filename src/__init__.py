from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .database import init_db
from .midleware.main import TokenMiddleware, ApiKeyMiddleware

from .routes.auth.main import auth
from .routes.token.main import token
from .routes.user.main import user
from .routes.crypto.main import crypto
from .routes.api_key.main import api_key


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

def create_app():
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.add_middleware(TokenMiddleware)
    app.add_middleware(ApiKeyMiddleware)

    app.include_router(auth)
    app.include_router(token)
    app.include_router(user)
    app.include_router(api_key)
    app.include_router(crypto)

    return app

