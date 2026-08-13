from pydantic import BaseModel, Field


class GeneratedRole(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None


class GeneratedSkill(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None

class GeneratedAIOpportunity(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None


class GeneratedActivity(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    roles: list[GeneratedRole] = Field(default_factory=list)
    skills: list[GeneratedSkill] = Field(default_factory=list)
    ai_opportunities: list[GeneratedAIOpportunity] = Field(
        default_factory=list
    )


class ProcessAnalysisRequest(BaseModel):
    instructions: str | None = None


class ProcessAnalysisResponse(BaseModel):
    process_name: str
    process_description: str | None = None
    activities: list[GeneratedActivity] = Field(default_factory=list)