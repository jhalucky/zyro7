from backend.app.agent.run import AgentRun
from backend.app.agent.state import AgentState
from backend.app.generation.generator import ProjectGenerator
from backend.app.planning.pipeline import PlanningPipeline
from backend.app.planning.plan import ApplicationPlan
from backend.app.repositories.agent_run import AgentRunRepository


class AgentRuntime:
    def __init__(
        self,
        planning_pipeline: PlanningPipeline,
        run_repository: AgentRunRepository,
        project_generator: ProjectGenerator,
    ):
        self.planning_pipeline = planning_pipeline
        self.run_repository = run_repository
        self.project_generator = project_generator

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