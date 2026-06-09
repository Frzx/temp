from dataclasses import dataclass

from sqlalchemy import select

from shared.database import Base,create_engine, create_session_factory
from shared.database.models import DocumentRecord

# This act as boundary between repsoitory and service layer
@dataclass(frozen=True, slots=True)
class StoredDocument:
    document_id: str
    document_type: str
    file_name: str
    content_type: str
    sha256: str
    s3_object_key: str
    s3_object_uri: str
    size_bytes: int

class DocumentsRepository:
    def __init__(self,database_url: str):
        self.engine = create_engine(database_url)
        self.session_factory = create_session_factory(self.engine)

    def initialize(self) -> None:
        Base.metadata.create_all(self.engine)

    def get_by_sha256(self, sha256: str) -> StoredDocument | None:
        with self.session_factory() as session:
            record = session.execute(
                select(DocumentRecord).where(DocumentRecord.sha256 ==  sha256)
            ).scalar_one_or_none()
        if record is None:
            return None
        
        return StoredDocument(
            document_id=record.document_id,
            document_type=record.document_type,
            file_name=record.file_name,
            content_type=record.content_type,
            sha256=record.sha256,
            s3_object_key=record.s3_object_key,
            s3_object_uri=record.s3_object_uri,
            size_bytes=record.size_bytes,
        )
    
    def insert(self, document: StoredDocument) -> None:
        with self.session_factory() as session:
            record = DocumentRecord(
                document_id=document.document_id,
                document_type=document.document_type,
                file_name=document.file_name,
                content_type=document.content_type,
                sha256=document.sha256,
                s3_object_key=document.s3_object_key,
                s3_object_uri=document.s3_object_uri,
                size_bytes=document.size_bytes,
            )
            session.add(record)
            session.commit()