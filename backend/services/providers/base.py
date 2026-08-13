from abc import ABC, abstractmethod

from app.schemas.process_analysis import (
    ProcessAnalysisRequest,
    ProcessAnalysisResponse,
)


class AIProvider(ABC):
    @abstractmethod
    def analyze_process(
        self,
        payload: ProcessAnalysisRequest,
    ) -> ProcessAnalysisResponse:
        raise NotImplementedError