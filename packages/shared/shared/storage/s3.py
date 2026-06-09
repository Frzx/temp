from pathlib import Path

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from shared.config import StorageSettings

class S3ObjectStorage:
    def __init__(self, settings: StorageSettings):
        self.settings = settings
        self.endpoint_url = settings.s3_endpoint_url
        self.bucket_name = settings.s3_bucket_name
        self.client: BaseClient = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint_url,
            region_name=settings.s3_region,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            use_ssl=settings.s3_use_ssl,
    )
        
    def ensure_bucket(self) -> None:
        try:
            self.client.head_bucket(Bucket = self.bucket_name)
        except ClientError:
            self.client.create_bucket(Bucket=self.bucket_name)

    def build_object_key(
        self,
        *,
        document_type: str,
        file_name: str,
        sha256: str,
    ) -> str:
        suffix = Path(file_name).suffix
        safe_name = Path(file_name).stem.replace(" ", "_")
        return f"{document_type}/{sha256}/{safe_name}{suffix}"

    def put_object(
        self,
        *,
        object_key: str,
        content: bytes,
        content_type: str,
    ) -> str:
        self.client.put_object(
            Bucket=self.bucket_name,
            Key=object_key,
            Body=content,
            ContentType=content_type,
        )
        if self.settings.s3_endpoint_url:
            return f"{self.settings.s3_endpoint_url.rstrip('/')}/{self.bucket_name}/{object_key}"
        return f"s3://{self.bucket_name}/{object_key}"
    