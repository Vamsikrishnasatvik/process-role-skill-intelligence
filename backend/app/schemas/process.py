import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProcessBase(BaseModel):
    name: str
    description: str | None = None
    metadata: dict = {}


class ProcessCreate(ProcessBase):
    value_chain_stage_id: uuid.UUID


class ProcessResponse(BaseModel):
    id: uuid.UUID
    value_chain_stage_id: uuid.UUID
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