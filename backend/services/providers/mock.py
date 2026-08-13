from app.schemas.process_analysis import (
    GeneratedActivity,
    GeneratedRole,
    GeneratedSkill,
    ProcessAnalysisRequest,
    ProcessAnalysisResponse,
)

from services.providers.base import AIProvider


class MockProvider(AIProvider):
    """
    Deterministic provider used for local development and tests.

    No external API calls are made.
    """

    def analyze_process(
        self,
        payload: ProcessAnalysisRequest,
    ) -> ProcessAnalysisResponse:

        activity = GeneratedActivity(
            name=f"Analyze {payload.name}",
            description=(
                f"Analyze the business activities involved in "
                f"{payload.name.lower()}."
            ),
            roles=[
                GeneratedRole(
                    name="Process Analyst",
                    description=(
                        "Analyzes process performance and supports "
                        "business improvement decisions."
                    ),
                )
            ],
            skills=[
                GeneratedSkill(
                    name="Process Analysis",
                    description=(
                        "Ability to analyze business processes, "
                        "identify patterns, and support improvements."
                    ),
                )
            ],
        )

        return ProcessAnalysisResponse(
            process_name=payload.name,
            process_description=payload.description,
            activities=[activity],
        )