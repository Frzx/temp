from redis.asyncio import Redis

# from shared.events import
from shared.contracts.events import DocumentUploadedEvent, DocumentUploadedPayload, EventMetadata
from shared.events import DOCUMENT_UPLOADED_STREAM, publish_event

class DocumentUploadedPublisher:
    def __init__(self,*, redis_client: Redis, producer_name: str):
        self.redis_client = redis_client
        self.producer_name = producer_name

    async def publish_document_uploaded(
            self,
            *,
            correlation_id: str,
            payload: DocumentUploadedPayload,
    ) -> str:
        event_metadata = EventMetadata(
            event_type= DOCUMENT_UPLOADED_STREAM,
            producer = self.producer_name,
            correlation_id = correlation_id,
        )
        event = DocumentUploadedEvent(
            metadata= event_metadata,
            payload = payload,
        )

        return await publish_event(
            self.redis_client,
            stream_name = DOCUMENT_UPLOADED_STREAM,
            event_json = event.model_dump_json(),
        )