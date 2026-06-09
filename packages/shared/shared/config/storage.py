from pydantic import Field

from .base import BaseAppSettings

class StorageSettings(BaseAppSettings):
    s3_endpoint_url: str | None = Field(default = None, alias= "S3_ENDPOINT_URL")
    s3_region: str = Field(alias = "S3_REGION")
    s3_access_key:str = Field(alias = "S3_ACCESS_KEY" )
    s3_secret_key: str = Field(alias = "S3_SECRET_KEY" )
    s3_bucket_name: str= Field(alias = "S3_BUCKET_NAME")
    s3_use_ssl: bool = Field(default = True, alias="S3_USE_SSL")
