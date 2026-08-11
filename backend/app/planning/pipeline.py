from backend.app.planning.analysis import (
    AnalysisStatus,
    RequirementAnalysis,
)
from backend.app.planning.analyzer import RequirementAnalyzer
from backend.app.planning.plan import PlanningResult, PlanningStatus
from backend.app.planning.planner import Planner
from backend.app.planning.validator import PlanValidator

class PlanningPipeline:
    def __init__(
        self,
        analyzer: RequirementAnalyzer,
        planner: Planner,
        validator: PlanValidator | None = None,
    ):
        self.analyzer = analyzer
        self.planner = planner
        self.validator = validator or PlanValidator()

    def run(self, requirement: str) -> PlanningResult:
        analysis = self.analyzer.analyze(requirement)

        if analysis.status == AnalysisStatus.NEEDS_CLARIFICATION:
            return PlanningResult(
                status=analysis.status,
                questions=analysis.questions,
            )

        planning_result = self.planner.create_plan(analysis)

        validation = self.validator.validate(
            analysis,
            planning_result,
        )

        if not validation.valid:
            return PlanningResult(
                status=PlanningStatus.VALIDATION_FAILED,
                plan=planning_result.plan,
                message="Generated plan failed validation.",
                validation_errors=validation.errors,
            )

        return planning_result