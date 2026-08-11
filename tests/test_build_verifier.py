from pathlib import Path

import pytest

from backend.app.execution.runner import ExecutionResult
from backend.app.execution.verifier import BuildVerifier
from backend.app.planning.plan import ApplicationPlan


class FakeRunner:
    def __init__(self, result):
        self.result = result
        self.command = None

    def run(self, command):
        self.command = command
        return self.result


def react_plan():
    return ApplicationPlan(
        name="Coffee Shop",
        description="A coffee shop landing page.",
        application_type="Web Application",
        framework="React",
        package_manager="npm",
    )


def nextjs_plan():
    return ApplicationPlan(
        name="Portfolio",
        description="A portfolio website.",
        application_type="Web Application",
        framework="Next.js",
        package_manager="npm",
    )


def test_verifier_runs_react_build(tmp_path):
    verifier = BuildVerifier(tmp_path)

    expected = ExecutionResult(
        success=True,
        exit_code=0,
        stdout="build successful",
        stderr="",
    )

    fake_runner = FakeRunner(expected)
    verifier.runner = fake_runner

    result = verifier.verify(react_plan())

    assert result is expected
    assert fake_runner.command == ["npm", "run", "build"]


def test_verifier_runs_nextjs_build(tmp_path):
    verifier = BuildVerifier(tmp_path)

    expected = ExecutionResult(
        success=True,
        exit_code=0,
        stdout="build successful",
        stderr="",
    )

    fake_runner = FakeRunner(expected)
    verifier.runner = fake_runner

    result = verifier.verify(nextjs_plan())

    assert result is expected
    assert fake_runner.command == ["npm", "run", "build"]


def test_verifier_returns_failed_build(tmp_path):
    verifier = BuildVerifier(tmp_path)

    expected = ExecutionResult(
        success=False,
        exit_code=1,
        stdout="",
        stderr="Build failed",
    )

    fake_runner = FakeRunner(expected)
    verifier.runner = fake_runner

    result = verifier.verify(react_plan())

    assert result.success is False
    assert result.exit_code == 1
    assert result.stderr == "Build failed"


def test_verifier_rejects_unsupported_framework(tmp_path):
    verifier = BuildVerifier(tmp_path)

    plan = ApplicationPlan(
        name="Example",
        description="Example application.",
        application_type="Web Application",
        framework="Angular",
        package_manager="npm",
    )

    with pytest.raises(ValueError):
        verifier.verify(plan)


def test_verifier_uses_workspace(tmp_path):
    verifier = BuildVerifier(tmp_path)

    assert verifier.workspace == Path(tmp_path).resolve()
    assert verifier.runner.workspace == Path(tmp_path).resolve()