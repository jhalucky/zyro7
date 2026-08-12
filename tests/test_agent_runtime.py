import pytest
from uuid import uuid4

from backend.app.agent.run import AgentRun
from backend.app.agent.runtime import AgentRuntime
from backend.app.agent.state import AgentState
from backend.app.execution.runner import ExecutionResult
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


class FakeBuildVerifier:
    def __init__(self, result):
        self.result = result
        self.plan = None

    def verify(self, plan):
        self.plan = plan
        return self.result


class FakeDependencyInstaller:
    def __init__(self, success=True):
        self.success = success
        self.called = False
        self.package_manager = None

    def install(self, package_manager):
        self.called = True
        self.package_manager = package_manager

        return ExecutionResult(
            success=self.success,
            exit_code=0 if self.success else 1,
            stdout="installed",
            stderr="" if self.success else "install failed",
        )


def create_runtime(
    pipeline,
    repository,
    generator,
    verifier,
    installer=None,
):
    if installer is None:
        installer = FakeDependencyInstaller()

    return AgentRuntime(
        planning_pipeline=pipeline,
        run_repository=repository,
        project_generator=generator,
        build_verifier=verifier,
        dependency_installer=installer,
    )


def successful_verifier():
    return FakeBuildVerifier(
        ExecutionResult(
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
        )
    )


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
    verifier = successful_verifier()
    installer = FakeDependencyInstaller()

    runtime = create_runtime(
        pipeline,
        repository,
        generator,
        verifier,
        installer,
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

    assert repository.updated_run is run


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
    verifier = successful_verifier()
    installer = FakeDependencyInstaller()

    runtime = create_runtime(
        pipeline,
        repository,
        generator,
        verifier,
        installer,
    )

    run = AgentRun(
        prompt="Build me something for a coffee shop."
    )

    runtime.plan(run)

    assert run.state == AgentState.PLANNING
    assert run.plan is None

    assert repository.updated_run is run
    assert installer.called is False


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
    verifier = successful_verifier()
    installer = FakeDependencyInstaller()

    runtime = create_runtime(
        pipeline,
        repository,
        generator,
        verifier,
        installer,
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
    verifier = successful_verifier()
    installer = FakeDependencyInstaller()

    runtime = create_runtime(
        pipeline,
        repository,
        generator,
        verifier,
        installer,
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
    verifier = successful_verifier()
    installer = FakeDependencyInstaller()

    runtime = create_runtime(
        pipeline,
        repository,
        generator,
        verifier,
        installer,
    )

    run = AgentRun(
        prompt="Create a coffee shop landing page."
    )

    runtime.plan(run)
    runtime.generate(run)

    assert generator.plan is not None
    assert generator.plan.name == "Coffee Shop"

    assert installer.called is True
    assert installer.package_manager == "npm"

    assert run.state == AgentState.GENERATED
    assert repository.updated_run is run


def test_runtime_rejects_generation_before_planning():
    repository = FakeAgentRunRepository()
    generator = FakeProjectGenerator()
    verifier = successful_verifier()
    installer = FakeDependencyInstaller()

    pipeline = FakePlanningPipeline(
        PlanningResult(
            status=PlanningStatus.NEEDS_CLARIFICATION,
            questions=[
                "What do you want to build?"
            ],
        )
    )

    runtime = create_runtime(
        pipeline,
        repository,
        generator,
        verifier,
        installer,
    )

    run = AgentRun(
        prompt="Build something."
    )

    assert run.state == AgentState.CREATED

    with pytest.raises(ValueError):
        runtime.generate(run)

    assert run.state == AgentState.CREATED
    assert generator.plan is None
    assert installer.called is False


def test_runtime_verifies_generated_project():
    planning_result = PlanningResult(
        status=PlanningStatus.READY,
        plan=ApplicationPlan(
            name="Coffee Shop",
            description="A coffee shop landing page.",
            application_type="Web Application",
            framework="React",
            package_manager="npm",
        ),
    )

    pipeline = FakePlanningPipeline(planning_result)
    repository = FakeAgentRunRepository()
    generator = FakeProjectGenerator()
    installer = FakeDependencyInstaller()

    build_result = ExecutionResult(
        success=True,
        exit_code=0,
        stdout="Build successful",
        stderr="",
    )

    verifier = FakeBuildVerifier(build_result)

    runtime = create_runtime(
        pipeline,
        repository,
        generator,
        verifier,
        installer,
    )

    run = AgentRun(
        prompt="Create a coffee shop landing page."
    )

    runtime.plan(run)
    runtime.generate(run)

    result = runtime.verify(run)

    assert result.success is True
    assert result.exit_code == 0

    assert run.state == AgentState.VERIFIED

    assert run.verification is not None
    assert run.verification["success"] is True
    assert run.verification["exit_code"] == 0

    assert verifier.plan is not None
    assert verifier.plan.name == "Coffee Shop"

    assert repository.updated_run is run


def test_runtime_marks_run_failed_when_build_fails():
    planning_result = PlanningResult(
        status=PlanningStatus.READY,
        plan=ApplicationPlan(
            name="Broken Project",
            description="A broken project.",
            application_type="Web Application",
            framework="React",
            package_manager="npm",
        ),
    )

    pipeline = FakePlanningPipeline(planning_result)
    repository = FakeAgentRunRepository()
    generator = FakeProjectGenerator()
    installer = FakeDependencyInstaller()

    build_result = ExecutionResult(
        success=False,
        exit_code=1,
        stdout="",
        stderr="Build failed",
    )

    verifier = FakeBuildVerifier(build_result)

    runtime = create_runtime(
        pipeline,
        repository,
        generator,
        verifier,
        installer,
    )

    run = AgentRun(
        prompt="Create a broken project."
    )

    runtime.plan(run)
    runtime.generate(run)

    result = runtime.verify(run)

    assert result.success is False
    assert result.exit_code == 1

    assert run.state == AgentState.FAILED

    assert run.verification is not None
    assert run.verification["success"] is False
    assert run.verification["exit_code"] == 1
    assert run.verification["stderr"] == "Build failed"

    assert repository.updated_run is run


def test_runtime_rejects_verification_before_generation():
    repository = FakeAgentRunRepository()
    generator = FakeProjectGenerator()
    verifier = successful_verifier()
    installer = FakeDependencyInstaller()

    pipeline = FakePlanningPipeline(
        PlanningResult(
            status=PlanningStatus.NEEDS_CLARIFICATION,
            questions=[
                "What do you want to build?"
            ],
        )
    )

    runtime = create_runtime(
        pipeline,
        repository,
        generator,
        verifier,
        installer,
    )

    run = AgentRun(
        prompt="Build something."
    )

    assert run.state == AgentState.CREATED

    with pytest.raises(ValueError):
        runtime.verify(run)

    assert run.state == AgentState.CREATED