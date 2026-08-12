import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AIOpportunityCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    metadata: dict = Field(default_factory=dict)


class AIOpportunityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    metadata: dict
    created_at: datetime
    updated_at: datetime