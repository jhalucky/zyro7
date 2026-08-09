import pytest
from pydantic import ValidationError

from backend.app.planning.plan import ApplicationPlan


def test_valid_application_plan():
    plan = ApplicationPlan(
        name="Coffee Shop",
        description="A coffee shop landing page",
        application_type="web",
        framework="Next.js",
        package_manager="npm",
        features=[
            "hero",
            "menu",
        ],
        pages=[
            "/",
        ],
        tasks=[
            "Initialize project",
            "Create landing page",
        ],
    )

    assert plan.name == "Coffee Shop"
    assert plan.framework == "Next.js"
    assert "hero" in plan.features


def test_missing_required_field_is_rejected():
    with pytest.raises(ValidationError):
        ApplicationPlan(
            name="Coffee Shop",
            description="A landing page",
            application_type="web",
            package_manager="npm",
        )


def test_empty_name_is_rejected():
    with pytest.raises(ValidationError):
        ApplicationPlan(
            name="",
            description="A landing page",
            application_type="web",
            framework="Next.js",
            package_manager="npm",
        )


def test_default_lists_are_empty():
    plan = ApplicationPlan(
        name="Coffee Shop",
        description="A landing page",
        application_type="web",
        framework="Next.js",
        package_manager="npm",
    )

    assert plan.features == []
    assert plan.pages == []
    assert plan.tasks == []