import hashlib
from dataclasses import asdict
from uuid import uuid4

from fastapi import UploadFile

from shared.contracts.events import DocumentUploadedPayload

from app.api.schemas import DocumentUploadedResponse
from app.messaging.publisher import DocumentUploadedPublisher
from app.repository.documents_repository import DocumentsRepository, StoredDocument
from app.storage import ObjectStorage

from .document_classifier import classify_document_type

class DocumentUploadService:
    def __init__(
        self,
        *,
        repository: DocumentsRepository,
        storage: ObjectStorage,
        publisher: DocumentUploadedPublisher,
    ) -> None:
        self.repository = repository
        self.storage = storage
        self.publisher = publisher

    @staticmethod
    def _build_response(document: StoredDocument, *, deduplicated: bool) -> DocumentUploadedResponse:
        return DocumentUploadedResponse(
            **asdict(document),
            deduplicated=deduplicated
        )
    
    async def _publish_document_uploaded(self,document: StoredDocument) -> None:
        await self.publisher.publish_document_uploaded(
            correlation_id = document.document_id,
            payload = DocumentUploadedPayload(**asdict(document))
        )
    async def upload_document(
            self,
            *,
            upload_file: UploadFile,
    ) -> DocumentUploadedResponse:
        if not upload_file.filename:
            raise ValueError("file name is requried")
        
        content = await upload_file.read()
        if not content:
            raise ValueError("empty fiels are not allowed")
        
        document_type = classify_document_type(
            file_name= upload_file.filename,
            content_type = upload_file.content_type,
        )

        sha256 = hashlib.sha256(content).hexdigest()
        existing = self.repository.get_by_sha256(sha256)
        if existing is not None:
            await self._publish_document_uploaded(existing)
            return self._build_response(existing, deduplicated=True)
        
        content_type = upload_file.content_type or "application/octet-stream"
        document_id = str(uuid4())
        object_key = self.storage.build_object_key(
            document_type=document_type,
            file_name = upload_file.filename,
            sha256= sha256,
        )
        object_uri = self.storage.put_object(
            object_key=object_key,
            content=content,
            content_type = content_type,
        )
        stored_document = StoredDocument(
            document_id=document_id,
            document_type=document_type,
            file_name=upload_file.filename,
            content_type=content_type,
            sha256=sha256,
            s3_object_key=object_key,
            s3_object_uri=object_uri,
            size_bytes=len(content),
        )
        self.repository.insert(stored_document)
        await self._publish_document_uploaded(stored_document)
        return self._build_response(stored_document, deduplicated=False)