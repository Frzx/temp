from pydantic import BaseModel

from .base import EventEnvelope

class DocumentUploadedPayload(BaseModel):
    document_id: str
    file_name: str
    document_type: str
    content_type: str
    sha256: str
    s3_object_key: str
    s3_object_uri: str
    size_bytes: int

class DocumentUploadedEvent(EventEnvelope[DocumentUploadedPayload]):
    pass
    

