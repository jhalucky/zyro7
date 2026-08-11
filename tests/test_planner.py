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


class FakePlannerModel(ModelProvider):
    def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            content="""
           {
                "status": "ready",
                "plan": {
                    "name": "Coffee Shop",
                    "description": "A modern coffee shop landing page",
                    "application_type": "web",
                    "framework": "Next.js",
                    "package_manager": "npm",
                    "features": [
                        "hero",
                        "menu",
                        "contact"
                    ],
                    "pages": [
                        "/"
                    ],
                    "tasks": [
                        "Initialize project",
                        "Create landing page",
                        "Run build"
                    ]
                }
            }
            """
        )


def test_planner_creates_application_plan():
    planner = Planner(FakePlannerModel())
    analysis = RequirementAnalysis(
        status=AnalysisStatus.READY,
        summary="A coffee shop landing page.",
        constraints=[], 
    )

    result = planner.create_plan(analysis)
    assert result.status == "ready"
    assert result.plan is not None

    


class InvalidModel(ModelProvider):
    def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            content="This is not JSON."
        )


def test_planner_rejects_invalid_json():
    planner = Planner(InvalidModel())

    analysis = RequirementAnalysis(
        status=AnalysisStatus.READY,
        summary="A coffee shop landing page.",
        constraints=[],
    )

    with pytest.raises(StructuredOutputError):
        planner.create_plan(analysis)



def test_planner_rejects_ambiguous_analysis():
    planner = Planner(FakePlannerModel())

    analysis = RequirementAnalysis(
        status=AnalysisStatus.NEEDS_CLARIFICATION,
        summary="A coffee shop application.",
        questions=[
            "What type of application do you want?"
        ],
    )

    with pytest.raises(ValueError):
        planner.create_plan(analysis)

class FakeParser:
    def __init__(self, result):
        self.result = result
        self.called = False
        self.content = None
        self.schema = None

    def parse(self, content, schema):
        self.called = True
        self.content = content
        self.schema = schema
        return self.result
    

def test_planner_uses_structured_output_parser():
    expected = PlanningResult(
        status=PlanningStatus.READY,
        plan=ApplicationPlan(
            name="Coffee Shop",
            description="A coffee shop landing page.",
            application_type="web",
            framework="React",
            package_manager="npm",
        ),
    )

    parser = FakeParser(expected)

    planner = Planner(
        FakePlannerModel(),
        parser=parser,
    )

    analysis = RequirementAnalysis(
        status=AnalysisStatus.READY,
        summary="A coffee shop landing page.",
        constraints=[],
    )

    result = planner.create_plan(analysis)

    assert result is expected
    assert parser.called is True
    assert parser.schema is PlanningResult