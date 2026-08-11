import sys

import pytest

from backend.app.execution.runner import (
    CommandExecutionError,
    ExecutionRunner,
)


def test_runner_executes_successful_command(tmp_path):
    runner = ExecutionRunner(tmp_path)

    result = runner.run(
        [sys.executable, "-c", "print('hello')"]
    )

    assert result.success is True
    assert result.exit_code == 0
    assert result.stdout.strip() == "hello"


def test_runner_captures_failed_command(tmp_path):
    runner = ExecutionRunner(tmp_path)

    result = runner.run(
        [sys.executable, "-c", "print('failure'); raise SystemExit(2)"]
    )

    assert result.success is False
    assert result.exit_code == 2
    assert "failure" in result.stdout


def test_runner_captures_stderr(tmp_path):
    runner = ExecutionRunner(tmp_path)

    result = runner.run(
        [
            sys.executable,
            "-c",
            "import sys; print('error', file=sys.stderr)",
        ]
    )

    assert result.success is True
    assert "error" in result.stderr


def test_runner_uses_workspace_as_working_directory(tmp_path):
    runner = ExecutionRunner(tmp_path)

    result = runner.run(
        [
            sys.executable,
            "-c",
            "from pathlib import Path; print(Path.cwd())",
        ]
    )

    assert result.success is True
    assert str(tmp_path) in result.stdout


def test_runner_passes_environment_variables(tmp_path):
    runner = ExecutionRunner(tmp_path)

    result = runner.run(
        [
            sys.executable,
            "-c",
            "import os; print(os.environ['VIBE_TEST'])",
        ],
        env={"VIBE_TEST": "hello"},
    )

    assert result.success is True
    assert result.stdout.strip() == "hello"


def test_runner_rejects_nonexistent_workspace(tmp_path):
    workspace = tmp_path / "does-not-exist"

    with pytest.raises(CommandExecutionError):
        ExecutionRunner(workspace)


def test_runner_timeout(tmp_path):
    runner = ExecutionRunner(tmp_path)

    result = runner.run(
        [
            sys.executable,
            "-c",
            "import time; time.sleep(2)",
        ],
        timeout=0.1,
    )

    assert result.success is False
    assert result.timed_out is True