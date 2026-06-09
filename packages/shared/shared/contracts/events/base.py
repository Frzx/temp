from typing import TypeVar, Generic
from uuid import uuid4
from datetime import datetime, UTC

from pydantic import BaseModel, Field

PayloadT = TypeVar("PayloadT",bound=BaseModel)

class EventMetadata(BaseModel):
    event_id: str = Field(default_factory = lambda : str(uuid4()))
    causation_id: str | None = Field(default=None)
    correlation_id: str
    event_type: str
    producer: str
    occurred_at: datetime = Field(default_factory = lambda: datetime.now(tz=UTC))
    schema_version: str = "1.0"

class EventEnvelope(BaseModel, Generic[PayloadT]):
    metadata: EventMetadata
    payload: PayloadT