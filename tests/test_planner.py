import pytest

from backend.app.model.base import ModelProvider
from backend.app.model.types import ModelRequest, ModelResponse
from backend.app.planning.planner import Planner


class FakePlannerModel(ModelProvider):
    def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            content="""
            {
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
            """
        )


def test_planner_creates_application_plan():
    planner = Planner(FakePlannerModel())

    plan = planner.create_plan(
        "Create a landing page for a coffee shop."
    )

    assert plan.name == "Coffee Shop"
    assert plan.application_type == "web"
    assert plan.framework == "Next.js"
    assert "hero" in plan.features
    assert "/" in plan.pages


class InvalidModel(ModelProvider):
    def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            content="This is not JSON."
        )


def test_planner_rejects_invalid_json():
    planner = Planner(InvalidModel())

    with pytest.raises(ValueError):
        planner.create_plan("Create a coffee shop landing page.")