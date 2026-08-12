from uuid import uuid4

from backend.app.agent.run import AgentRun
from backend.app.agent.service import AgentService
from backend.app.agent.state import AgentState
from backend.app.planning.plan import (
    ApplicationPlan,
    PlanningResult,
    PlanningStatus,
)


class FakeAgentRuntime:
    def __init__(self, planning_result):
        self.planning_result = planning_result
        self.plan_called = False
        self.generate_called = False
        self.verify_called = False

    def plan(self, run: AgentRun) -> None:
        self.plan_called = True

        run.transition_to(AgentState.PLANNING)

        if self.planning_result.plan is None:
            return

        run.plan = self.planning_result.plan.model_dump()

        run.transition_to(AgentState.PLANNED)

    def generate(self, run: AgentRun) -> None:
        self.generate_called = True

        run.transition_to(AgentState.GENERATING)
        run.transition_to(AgentState.GENERATED)

    def verify(self, run: AgentRun) -> None:
        self.verify_called = True

        run.transition_to(AgentState.VERIFYING)
        run.transition_to(AgentState.VERIFIED)


def test_service_executes_planned_run():
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

    runtime = FakeAgentRuntime(result)
    service = AgentService(runtime)

    run = AgentRun(
        prompt="Create a coffee shop landing page.",
        project_id=uuid4(),
    )

    result = service.execute(run)

    assert result is run

    assert runtime.plan_called is True
    assert runtime.generate_called is True
    assert runtime.verify_called is True

    assert run.state == AgentState.VERIFIED
    assert run.plan is not None
    assert run.plan["name"] == "Coffee Shop"


def test_service_stops_when_clarification_is_needed():
    result = PlanningResult(
        status=PlanningStatus.NEEDS_CLARIFICATION,
        questions=[
            "What type of application do you want?"
        ],
    )

    runtime = FakeAgentRuntime(result)
    service = AgentService(runtime)

    run = AgentRun(
        prompt="Build me something for a coffee shop.",
    )

    result = service.execute(run)

    assert result is run

    assert runtime.plan_called is True
    assert runtime.generate_called is False
    assert runtime.verify_called is False

    assert run.state == AgentState.PLANNING
    assert run.plan is None


def test_service_rejects_empty_prompt():
    runtime = FakeAgentRuntime(
        PlanningResult(
            status=PlanningStatus.NEEDS_CLARIFICATION,
        )
    )

    service = AgentService(runtime)

    run = AgentRun(prompt="")

    try:
        service.execute(run)
        assert False
    except ValueError as exc:
        assert str(exc) == "Prompt cannot be empty."