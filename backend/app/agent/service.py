from backend.app.agent.run import AgentRun
from backend.app.agent.runtime import AgentRuntime
from backend.app.agent.state import AgentState


class AgentService:
    def __init__(self, runtime: AgentRuntime):
        self.runtime = runtime

    def execute(self, run: AgentRun) -> AgentRun:
        if not run.prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        self.runtime.plan(run)

        if run.state != AgentState.PLANNED:
            return run

        self.runtime.generate(run)

        if run.state != AgentState.GENERATED:
            return run

        self.runtime.verify(run)

        return run