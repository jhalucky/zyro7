import pytest

from backend.app.model.base import ModelProvider
from backend.app.model.types import ModelRequest, ModelResponse
from backend.app.planning.planner import Planner


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

    result = planner.create_plan(
    "Create a landing page for a coffee shop."
)

    assert result.status == "ready"
    assert result.plan is not None

    assert result.plan.name == "Coffee Shop"
    assert result.plan.application_type == "web"
    assert result.plan.framework == "Next.js"
    assert "hero" in result.plan.features
    assert "/" in result.plan.pages


class InvalidModel(ModelProvider):
    def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            content="This is not JSON."
        )


def test_planner_rejects_invalid_json():
    planner = Planner(InvalidModel())

    with pytest.raises(ValueError):
        planner.create_plan("Create a coffee shop landing page.")


class ClarificationModel(ModelProvider):
    def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            content="""
            {
                "status": "needs_clarification",
                "questions": [
                    "What type of coffee shop application do you want to build?"
                ]
            }
            """
        )


def test_planner_can_request_clarification():
    planner = Planner(ClarificationModel())

    result = planner.create_plan(
        "Build me something for a coffee shop."
    )

    assert result.status == "needs_clarification"
    assert result.plan is None
    assert len(result.questions) == 1