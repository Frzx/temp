from pydantic import BaseModel

class DocumentUploadedResponse(BaseModel):
    document_id: str
    document_type: str
    file_name: str
    content_type: str
    sha256: str
    s3_object_key: str
    s3_object_uri: str
    size_bytes: int
    deduplicated: bool