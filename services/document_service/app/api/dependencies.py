from fastapi import Request
from redis.asyncio import Redis

from shared.events import close_redis_client, create_connection

from app.config import AppSettings
from app.messaging.publisher import DocumentUploadedPublisher
from app.repository.documents_repository import DocumentsRepository
from app.services.document_upload_service import DocumentUploadService
from app.storage.object_storage import ObjectStorage

def build_upload_service() -> tuple[DocumentUploadService, Redis]:
    settings = AppSettings()
    repository = DocumentsRepository(settings.document_service.database_url)
    repository.initialize() # creates the tables if not created

    storage = ObjectStorage(settings.storage)
    storage.ensure_bucket()

    redis_client = create_connection(settings.messaging.redis_url)
    publisher = DocumentUploadedPublisher(
        redis_client= redis_client,
        producer_name = settings.document_service.service_name,
    )
    upload_service = DocumentUploadService(
        repository = repository,
        storage = storage,
        publisher = publisher,
    )
    
    return upload_service, redis_client

async def close_redis(redis: Redis) -> None:
    await close_redis_client(redis)


def get_upload_service(request: Request) -> DocumentUploadService:
    return request.app.state.upload_service