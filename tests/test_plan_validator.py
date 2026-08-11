import pytest
from backend.app.planning.analysis import (
    AnalysisStatus,
    RequirementAnalysis,
)
from backend.app.structured.errors import StructuredOutputError
from backend.app.model.base import ModelProvider
from backend.app.model.types import ModelRequest, ModelResponse
from backend.app.planning.planner import Planner
from backend.app.planning.plan import (
    ApplicationPlan,
    PlanningResult,
    PlanningStatus,
)
from backend.app.planning.validator import PlanValidator

def test_validator_accepts_valid_plan():
    analysis = RequirementAnalysis(
        status=AnalysisStatus.READY,
        summary="A coffee shop landing page.",
        constraints=[],
    )

    plan = ApplicationPlan(
        name="Coffee Shop Landing Page",
        description="A modern landing page.",
        application_type="Web Application",
        framework="React",
        package_manager="npm",
        requirements=[
            "Create a modern landing page for a coffee shop."
        ],
        assumptions=[],
        features=[
            "Hero section",
            "Menu section",
        ],
        pages=[
            "Landing Page",
        ],
        tasks=[
            "Create React project",
            "Build landing page",
        ],
    )

    planning_result = PlanningResult(
        status=PlanningStatus.READY,
        plan=plan,
    )

    validator = PlanValidator()

    result = validator.validate(
        analysis,
        planning_result,
    )

    assert result.valid is True
    assert result.errors == []



def test_validator_rejects_clarification():
    analysis = RequirementAnalysis(
        status=AnalysisStatus.NEEDS_CLARIFICATION,
        summary="A coffee shop application.",
        questions=[
            "What type of application?"
        ],
    )

    planning_result = PlanningResult(
        status=PlanningStatus.NEEDS_CLARIFICATION,
        questions=[
            "What type of application?"
        ],
    )

    validator = PlanValidator()

    result = validator.validate(
        analysis,
        planning_result,
    )

    assert result.valid is False
    assert result.errors


def test_validator_rejects_ready_result_without_plan():
    analysis = RequirementAnalysis(
        status=AnalysisStatus.READY,
        summary="A coffee shop landing page.",
        constraints=[],
    )

    planning_result = PlanningResult(
        status=PlanningStatus.READY,
        plan=None,
    )

    validator = PlanValidator()

    result = validator.validate(
        analysis,
        planning_result,
    )

    assert result.valid is False


def test_validator_rejects_ready_result_without_plan():
    analysis = RequirementAnalysis(
        status=AnalysisStatus.READY,
        summary="A coffee shop landing page.",
        constraints=[],
    )

    planning_result = PlanningResult(
        status=PlanningStatus.READY,
        plan=None,
    )

    validator = PlanValidator()

    result = validator.validate(
        analysis,
        planning_result,
    )

    assert result.valid is False

def test_validator_rejects_framework_constraint_violation():
    analysis = RequirementAnalysis(
        status=AnalysisStatus.READY,
        summary="Create a portfolio website.",
        constraints=["Next.js"],
    )

    plan = ApplicationPlan(
        name="Portfolio",
        description="A portfolio website.",
        application_type="Web Application",
        framework="React",
        package_manager="npm",
        requirements=[
            "Create a portfolio website."
        ],
        assumptions=[],
        features=[
            "Portfolio sections",
        ],
        pages=[
            "Home",
        ],
        tasks=[
            "Create portfolio",
        ],
    )

    planning_result = PlanningResult(
        status=PlanningStatus.READY,
        plan=plan,
    )

    validator = PlanValidator()

    result = validator.validate(
        analysis,
        planning_result,
    )

    assert result.valid is False
    assert any(
        "Next.js" in error
        for error in result.errors
    )