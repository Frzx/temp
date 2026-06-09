from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.dependencies import build_upload_service, close_redis
from app.api.routers import documents

@asynccontextmanager
async def lifespan(app: FastAPI):
    upload_service,redis_client = build_upload_service()
    app.state.upload_service = upload_service
    try:
        yield
    finally:
        await close_redis(redis_client)

app = FastAPI(
    title="Document Service",
    lifespan = lifespan,
)
app.include_router(documents.router)
