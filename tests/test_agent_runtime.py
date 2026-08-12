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

    runtime = AgentRuntime(
        planning_pipeline=pipeline,
        run_repository=repository,
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

    runtime = AgentRuntime(
        planning_pipeline=pipeline,
        run_repository=repository,
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

    runtime = AgentRuntime(
        planning_pipeline=pipeline,
        run_repository=repository,
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

    runtime = AgentRuntime(
        planning_pipeline=pipeline,
        run_repository=repository,
    )

    run = AgentRun(
        prompt="Build me something for a coffee shop."
    )

    runtime.plan(run)

    assert repository.updated_run is run
    assert repository.updated_run.state == AgentState.PLANNING
    assert repository.updated_run.plan is None