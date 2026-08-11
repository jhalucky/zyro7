from backend.app.structured.parser import StructuredOutputParser

from backend.app.model.base import ModelProvider
from backend.app.model.types import Message, ModelRequest
from backend.app.planning.analysis import AnalysisStatus, RequirementAnalysis
from backend.app.planning.plan import PlanningResult
from backend.app.planning.prompts import (
    PLANNER_SYSTEM_PROMPT,
    build_planner_prompt,
)


class Planner:
    def __init__(self, model: ModelProvider, parser: StructuredOutputParser | None = None):
        self.model = model
        self.parser = parser or StructuredOutputParser()

    def create_plan(
        self,
        analysis: RequirementAnalysis,
    ) -> PlanningResult:
        if analysis.status != AnalysisStatus.READY:
            raise ValueError(
                "Planner requires a READY requirement analysis."
            )

        request = ModelRequest(
            messages=[
                Message(
                    role="system",
                    content=PLANNER_SYSTEM_PROMPT,
                ),
                Message(
                    role="user",
                    content=build_planner_prompt(analysis),
                ),
            ],
            temperature=0.2,
        )

        response = self.model.generate(request)

        return self.parser.parse(
            response.content,
            PlanningResult,
        )