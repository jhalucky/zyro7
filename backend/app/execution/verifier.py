from pathlib import Path

from backend.app.execution.runner import (
    ExecutionResult,
    ExecutionRunner,
)
from backend.app.planning.plan import ApplicationPlan


class BuildVerifier:
    def __init__(self, workspace: Path):
        self.workspace = Path(workspace).resolve()
        self.runner = ExecutionRunner(self.workspace)

    def verify(self, plan: ApplicationPlan) -> ExecutionResult:
        framework = plan.framework.lower()

        if framework in {"react", "react.js"}:
            command = ["npm", "run", "build"]

        elif framework in {"next.js", "nextjs"}:
            command = ["npm", "run", "build"]

        else:
            raise ValueError(
                f"Unsupported framework: {plan.framework}"
            )

        return self.runner.run(command)