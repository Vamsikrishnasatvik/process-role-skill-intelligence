import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ActivityBase(BaseModel):
    name: str
    description: str | None = None
    metadata: dict = {}


class ActivityCreate(ActivityBase):
    process_id: uuid.UUID


class ActivityResponse(BaseModel):
    id: uuid.UUID
    process_id: uuid.UUID
    name: str
    description: str | None = None

    metadata: dict = Field(
        validation_alias="metadata_",
        serialization_alias="metadata",
    )

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )