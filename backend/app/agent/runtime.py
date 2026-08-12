from backend.app.agent.run import AgentRun
from backend.app.agent.state import AgentState
from backend.app.generation.generator import ProjectGenerator
from backend.app.planning.pipeline import PlanningPipeline
from backend.app.planning.plan import ApplicationPlan
from backend.app.repositories.agent_run import AgentRunRepository
from backend.app.execution.verifier import BuildVerifier
from backend.app.execution.runner import ExecutionResult


class AgentRuntime:
    def __init__(
        self,
        planning_pipeline: PlanningPipeline,
        run_repository: AgentRunRepository,
        project_generator: ProjectGenerator,
        build_verifier: BuildVerifier,
    ):
        self.planning_pipeline = planning_pipeline
        self.run_repository = run_repository
        self.project_generator = project_generator
        self.build_verifier = build_verifier

    def plan(self, run: AgentRun) -> None:
        run.transition_to(AgentState.PLANNING)

        result = self.planning_pipeline.run(run.prompt)

        if result.plan is None:
            self.run_repository.update(run)
            return

        run.plan = result.plan.model_dump()

        run.transition_to(AgentState.PLANNED)

        self.run_repository.update(run)

    def generate(self, run: AgentRun) -> None:
        if run.state != AgentState.PLANNED:
            raise ValueError(
                "Agent run must be PLANNED before generation."
            )

        if run.plan is None:
            raise ValueError(
                "Agent run has no plan to generate."
            )

        run.transition_to(AgentState.GENERATING)

        plan = ApplicationPlan.model_validate(run.plan)

        self.project_generator.generate(plan)

        run.transition_to(AgentState.GENERATED)

        self.run_repository.update(run)

    def verify(self, run: AgentRun) -> ExecutionResult:
        if run.state != AgentState.GENERATED:
            raise ValueError(
                "Agent run must be GENERATED before verification."
            )

        if run.plan is None:
            raise ValueError(
                "Agent run has no plan to verify."
            )

        run.transition_to(AgentState.VERIFYING)

        plan = ApplicationPlan.model_validate(run.plan)

        result = self.build_verifier.verify(plan)

        run.verification = {
            "success": result.success,
            "exit_code": result.exit_code,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "timed_out": result.timed_out,
        }

        if result.success:
            run.transition_to(AgentState.VERIFIED)
        else:
            run.transition_to(AgentState.FAILED)

        self.run_repository.update(run)

        return result