import os

from app.schemas.process_analysis import (
    ProcessAnalysisRequest,
    ProcessAnalysisResponse,
)

from services.providers.base import AIProvider
from services.providers.mock import MockProvider


class AIService:
    def __init__(self, provider: AIProvider | None = None):
        self.provider = provider or self._create_provider()

    def _create_provider(self) -> AIProvider:
        provider_name = os.getenv(
            "AI_PROVIDER",
            "mock",
        ).lower()

        if provider_name == "mock":
            return MockProvider()

        raise ValueError(
            f"Unsupported AI provider: {provider_name}"
        )

    def analyze_process(
        self,
        process_name: str,
        process_description: str | None,
        payload: ProcessAnalysisRequest,
    ) -> ProcessAnalysisResponse:
        return self.provider.analyze_process(
            process_name=process_name,
            process_description=process_description,
            payload=payload,
        )


ai_service = AIService()