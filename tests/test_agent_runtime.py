import pytest
from uuid import uuid4

from backend.app.agent.run import AgentRun
from backend.app.agent.runtime import AgentRuntime
from backend.app.agent.state import AgentState
from backend.app.planning.plan import (
    ApplicationPlan,
    PlanningResult,
    PlanningStatus,
)


class FakePlanningPipeline:
    def __init__(self, result):
        self.result = result
        self.requirement = None

    def run(self, requirement):
        self.requirement = requirement
        return self.result


class FakeAgentRunRepository:
    def __init__(self):
        self.updated_run = None

    def update(self, run):
        self.updated_run = run
        return run


class FakeProjectGenerator:
    def __init__(self):
        self.plan = None

    def generate(self, plan):
        self.plan = plan


def test_runtime_plans_agent_run():
    result = PlanningResult(
        status=PlanningStatus.READY,
        plan=ApplicationPlan(
            name="Coffee Shop",
            description="A coffee shop landing page.",
            application_type="Web Application",
            framework="React",
            package_manager="npm",
        ),
    )

    pipeline = FakePlanningPipeline(result)
    repository = FakeAgentRunRepository()
    generator = FakeProjectGenerator()

    runtime = AgentRuntime(
        planning_pipeline=pipeline,
        run_repository=repository,
        project_generator=generator,
    )

    run = AgentRun(
        prompt="Create a coffee shop landing page.",
        project_id=uuid4(),
    )

    runtime.plan(run)

    assert pipeline.requirement == (
        "Create a coffee shop landing page."
    )

    assert run.state == AgentState.PLANNED
    assert run.plan is not None
    assert run.plan["name"] == "Coffee Shop"


def test_runtime_keeps_run_in_planning_when_clarification_is_needed():
    result = PlanningResult(
        status=PlanningStatus.NEEDS_CLARIFICATION,
        questions=[
            "What type of application do you want?"
        ],
    )

    pipeline = FakePlanningPipeline(result)
    repository = FakeAgentRunRepository()
    generator = FakeProjectGenerator()

    runtime = AgentRuntime(
        planning_pipeline=pipeline,
        run_repository=repository,
        project_generator=generator,
    )

    run = AgentRun(
        prompt="Build me something for a coffee shop."
    )

    runtime.plan(run)

    assert run.state == AgentState.PLANNING
    assert run.plan is None


def test_runtime_persists_planned_run():
    result = PlanningResult(
        status=PlanningStatus.READY,
        plan=ApplicationPlan(
            name="Coffee Shop",
            description="A coffee shop landing page.",
            application_type="Web Application",
            framework="React",
            package_manager="npm",
        ),
    )

    pipeline = FakePlanningPipeline(result)
    repository = FakeAgentRunRepository()
    generator = FakeProjectGenerator()

    runtime = AgentRuntime(
        planning_pipeline=pipeline,
        run_repository=repository,
        project_generator=generator,
    )

    run = AgentRun(
        prompt="Create a coffee shop landing page."
    )

    runtime.plan(run)

    assert repository.updated_run is run
    assert repository.updated_run.state == AgentState.PLANNED
    assert repository.updated_run.plan is not None
    assert repository.updated_run.plan["name"] == "Coffee Shop"


def test_runtime_persists_clarification_state():
    result = PlanningResult(
        status=PlanningStatus.NEEDS_CLARIFICATION,
        questions=[
            "What type of application do you want?"
        ],
    )

    pipeline = FakePlanningPipeline(result)
    repository = FakeAgentRunRepository()
    generator = FakeProjectGenerator()

    runtime = AgentRuntime(
        planning_pipeline=pipeline,
        run_repository=repository,
        project_generator=generator,
    )

    run = AgentRun(
        prompt="Build me something for a coffee shop."
    )

    runtime.plan(run)

    assert repository.updated_run is run
    assert repository.updated_run.state == AgentState.PLANNING
    assert repository.updated_run.plan is None


def test_runtime_generates_project():
    result = PlanningResult(
        status=PlanningStatus.READY,
        plan=ApplicationPlan(
            name="Coffee Shop",
            description="A coffee shop landing page.",
            application_type="Web Application",
            framework="React",
            package_manager="npm",
        ),
    )

    pipeline = FakePlanningPipeline(result)
    repository = FakeAgentRunRepository()
    generator = FakeProjectGenerator()

    runtime = AgentRuntime(
        planning_pipeline=pipeline,
        run_repository=repository,
        project_generator=generator,
    )

    run = AgentRun(
        prompt="Create a coffee shop landing page."
    )

    runtime.plan(run)
    runtime.generate(run)

    assert generator.plan is not None
    assert generator.plan.name == "Coffee Shop"
    assert generator.plan.framework == "React"

    assert run.state == AgentState.GENERATED
    assert run.plan is not None
    assert run.plan["name"] == "Coffee Shop"

    assert repository.updated_run is run


def test_runtime_rejects_generation_before_planning():
    repository = FakeAgentRunRepository()
    generator = FakeProjectGenerator()

    pipeline = FakePlanningPipeline(
        PlanningResult(
            status=PlanningStatus.NEEDS_CLARIFICATION,
            questions=[
                "What do you want to build?"
            ],
        )
    )

    runtime = AgentRuntime(
        planning_pipeline=pipeline,
        run_repository=repository,
        project_generator=generator,
    )

    run = AgentRun(
        prompt="Build something."
    )

    assert run.state == AgentState.CREATED

    with pytest.raises(ValueError):
        runtime.generate(run)

    assert run.state == AgentState.CREATED
    assert generator.plan is None