from app.schemas.process_analysis import (
    GeneratedActivity,
    GeneratedAIOpportunity,
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
        process_name: str,
        process_description: str | None,
        payload: ProcessAnalysisRequest,
    ) -> ProcessAnalysisResponse:

        activity = GeneratedActivity(
            name=f"Analyze {process_name}",
            description=(
                f"Analyze the business activities involved in "
                f"{process_name.lower()}."
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
            ai_opportunities=[
                GeneratedAIOpportunity(
                    name="AI-Assisted Process Optimization",
                    description=(
                        "Use AI to analyze process data, identify improvement "
                        "opportunities, and support decision-making."
                    ),
                )
            ],
        )

        return ProcessAnalysisResponse(
            process_name=process_name,
            process_description=process_description,
            activities=[activity],
        )