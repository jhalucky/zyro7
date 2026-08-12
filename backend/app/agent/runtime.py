from backend.app.agent.run import AgentRun
from backend.app.agent.state import AgentState
from backend.app.planning.pipeline import PlanningPipeline
from backend.app.repositories.agent_run import AgentRunRepository


class AgentRuntime:
    def __init__(
        self,
        planning_pipeline: PlanningPipeline,
        run_repository: AgentRunRepository,
    ):
        self.planning_pipeline = planning_pipeline
        self.run_repository = run_repository

    def plan(self, run: AgentRun) -> None:
        run.transition_to(AgentState.PLANNING)

        result = self.planning_pipeline.run(run.prompt)

        if result.plan is None:
            self.run_repository.update(run)
            return

        run.plan = result.plan.model_dump()

        run.transition_to(AgentState.PLANNED)

        self.run_repository.update(run)