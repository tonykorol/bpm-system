from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api import router
from src.services.auth import auth_service_singleton

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await auth_service_singleton.initialize()
    yield
    await auth_service_singleton.close()


app.include_router(router, prefix="/api")
