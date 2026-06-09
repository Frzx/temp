from pydantic import Field

from .base import BaseAppSettings

class MessagingSettings(BaseAppSettings):
    redis_url: str = Field(
        default = 'redis://localhost:6379/0',
        alias='REDIS_URL',
    )