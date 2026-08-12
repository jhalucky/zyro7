from pathlib import Path

from backend.app.execution.runner import (
    ExecutionResult,
    ExecutionRunner,
)


class DependencyInstaller:
    def __init__(self, workspace: Path):
        self.workspace = Path(workspace).resolve()
        self.runner = ExecutionRunner(self.workspace)

    def install(
        self,
        package_manager: str,
    ) -> ExecutionResult:
        package_manager = package_manager.lower()

        if package_manager == "npm":
            command = ["npm", "install"]
        else:
            raise ValueError(
                f"Unsupported package manager: {package_manager}"
            )

        return self.runner.run(command)