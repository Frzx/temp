from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base

class DocumentRecord(Base):
    __tablename__ = "documents"
    
    document_id: Mapped[str] = mapped_column(String,primary_key=True)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    document_type: Mapped[str] = mapped_column(String, nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=False)
    sha256: Mapped[str] = mapped_column(String, nullable=False, unique = True)
    s3_object_key: Mapped[str] = mapped_column(String, nullable=False)
    s3_object_uri: Mapped[str] = mapped_column(String, nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)