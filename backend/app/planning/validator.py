from pydantic import BaseModel, Field

from backend.app.planning.analysis import (
    AnalysisStatus,
    RequirementAnalysis,
)
from backend.app.planning.plan import (
    PlanningResult,
    PlanningStatus,
)


class PlanValidationResult(BaseModel):
    valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class PlanValidator:
    def validate(
        self,
        analysis: RequirementAnalysis,
        planning_result: PlanningResult,
    ) -> PlanValidationResult:

        errors: list[str] = []
        warnings: list[str] = []

        if analysis.status != AnalysisStatus.READY:
            errors.append(
                "Cannot validate a plan for a requirement "
                "that needs clarification."
            )

        if planning_result.status != PlanningStatus.READY:
            errors.append(
                "Planning result is not ready."
            )

        if planning_result.plan is None:
            errors.append(
                "Planning result does not contain an application plan."
            )

            return PlanValidationResult(
                valid=False,
                errors=errors,
                warnings=warnings,
            )

        plan = planning_result.plan

        if not plan.features and not plan.pages and not plan.tasks:
            errors.append(
                "Application plan contains no implementation details."
            )

        self._validate_constraints(
            analysis,
            plan,
            errors,
        )

        return PlanValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )

    @staticmethod
    def _validate_constraints(
        analysis: RequirementAnalysis,
        plan,
        errors: list[str],
    ) -> None:

        framework_constraints = [
            constraint
            for constraint in analysis.constraints
            if constraint.lower()
            in {
                "react",
                "react.js",
                "next.js",
                "nextjs",
                "vue",
                "angular",
            }
        ]

        if framework_constraints:
            requested = framework_constraints[0].lower()
            actual = plan.framework.lower()

            if requested not in actual and actual not in requested:
                errors.append(
                    f"Requested framework "
                    f"'{framework_constraints[0]}' "
                    f"but plan uses '{plan.framework}'."
                )