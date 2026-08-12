from pathlib import Path

from backend.app.execution.installer import DependencyInstaller


class FakeRunner:
    def __init__(self):
        self.command = None

    def run(self, command):
        self.command = command

        from backend.app.execution.runner import ExecutionResult

        return ExecutionResult(
            success=True,
            exit_code=0,
            stdout="installed",
            stderr="",
        )


def test_installer_uses_npm_install(tmp_path):
    installer = DependencyInstaller(tmp_path)

    fake_runner = FakeRunner()
    installer.runner = fake_runner

    result = installer.install("npm")

    assert fake_runner.command == [
        "npm",
        "install",
    ]

    assert result.success is True

def test_installer_rejects_unsupported_package_manager(tmp_path):
    installer = DependencyInstaller(tmp_path)

    try:
        installer.install("unknown")
        assert False
    except ValueError as exc:
        assert "Unsupported package manager" in str(exc)

        