from backend.app.planning.analysis import (
    AnalysisStatus,
    RequirementAnalysis,
)
from backend.app.planning.analyzer import RequirementAnalyzer
from backend.app.planning.plan import PlanningResult
from backend.app.planning.planner import Planner


class PlanningPipeline:
    def __init__(
        self,
        analyzer: RequirementAnalyzer,
        planner: Planner,
    ):
        self.analyzer = analyzer
        self.planner = planner

    def run(self, requirement: str) -> PlanningResult:
        analysis = self.analyzer.analyze(requirement)

        if analysis.status == AnalysisStatus.NEEDS_CLARIFICATION:
            return PlanningResult(
                status=analysis.status,
                questions=analysis.questions,
            )

        return self.planner.create_plan(analysis)