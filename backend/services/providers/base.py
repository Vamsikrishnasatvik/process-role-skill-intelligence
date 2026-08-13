from abc import ABC, abstractmethod

from app.schemas.process_analysis import (
    ProcessAnalysisRequest,
    ProcessAnalysisResponse,
)


class AIProvider(ABC):
    @abstractmethod
    def analyze_process(
        self,
        process_name: str,
        process_description: str | None,
        payload: ProcessAnalysisRequest,
    ) -> ProcessAnalysisResponse:
        raise NotImplementedError