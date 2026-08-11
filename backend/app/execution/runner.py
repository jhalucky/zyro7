from dataclasses import dataclass
from pathlib import Path
import os
import subprocess


class CommandExecutionError(Exception):
    """Raised when command execution cannot be started."""


@dataclass
class ExecutionResult:
    success: bool
    exit_code: int | None
    stdout: str
    stderr: str
    timed_out: bool = False


class ExecutionRunner:
    def __init__(self, workspace: Path):
        self.workspace = Path(workspace).resolve()

        if not self.workspace.exists():
            raise CommandExecutionError(
                f"Workspace does not exist: {self.workspace}"
            )

        if not self.workspace.is_dir():
            raise CommandExecutionError(
                f"Workspace is not a directory: {self.workspace}"
            )

    def run(
        self,
        command: list[str],
        *,
        timeout: float | None = None,
        env: dict[str, str] | None = None,
    ) -> ExecutionResult:
        if not command:
            raise CommandExecutionError(
                "Command cannot be empty."
            )

        process_env = os.environ.copy()

        if env:
            process_env.update(env)

        try:
            completed = subprocess.run(
                command,
                cwd=self.workspace,
                env=process_env,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )

            return ExecutionResult(
                success=completed.returncode == 0,
                exit_code=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
            )

        except subprocess.TimeoutExpired as exc:
            stdout = self._decode_output(exc.stdout)
            stderr = self._decode_output(exc.stderr)

            return ExecutionResult(
                success=False,
                exit_code=None,
                stdout=stdout,
                stderr=stderr,
                timed_out=True,
            )

        except (OSError, subprocess.SubprocessError) as exc:
            raise CommandExecutionError(
                f"Failed to execute command: {exc}"
            ) from exc

    @staticmethod
    def _decode_output(output) -> str:
        if output is None:
            return ""

        if isinstance(output, bytes):
            return output.decode(
                "utf-8",
                errors="replace",
            )

        return output