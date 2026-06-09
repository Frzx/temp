from pydantic import Field

from shared.config import BaseAppSettings, MessagingSettings, StorageSettings

class DocumentServiceSettings(BaseAppSettings):
    service_name: str = "document_service"
    database_url: str = Field(
        "postgresql+psycopg://postgres:postgres@localhost:5432/document_service",
        alias = "DATABASE_URL",
    )

class AppSettings(BaseAppSettings):
    messaging: MessagingSettings = MessagingSettings()
    storage: StorageSettings = StorageSettings()
    document_service: DocumentServiceSettings = DocumentServiceSettings()