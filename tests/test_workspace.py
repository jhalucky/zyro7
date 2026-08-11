from pathlib import Path

import pytest

from backend.app.workspace.manager import (
    WorkspaceError,
    WorkspaceManager,
)


def test_workspace_create(tmp_path):
    workspace_path = tmp_path / "project"

    workspace = WorkspaceManager(workspace_path)

    workspace.create()

    assert workspace_path.exists()
    assert workspace_path.is_dir()


def test_workspace_write_and_read_file(tmp_path):
    workspace = WorkspaceManager(tmp_path / "project")
    workspace.create()

    workspace.write_file(
        "hello.txt",
        "Hello, workspace!",
    )

    assert workspace.exists("hello.txt")
    assert workspace.read_file("hello.txt") == "Hello, workspace!"


def test_workspace_creates_nested_directories(tmp_path):
    workspace = WorkspaceManager(tmp_path / "project")
    workspace.create()

    workspace.write_file(
        "src/components/App.jsx",
        "export default function App() {}",
    )

    assert workspace.exists("src/components/App.jsx")
    assert (
        workspace.read_file("src/components/App.jsx")
        == "export default function App() {}"
    )


def test_workspace_rejects_parent_path_traversal(tmp_path):
    workspace = WorkspaceManager(tmp_path / "project")
    workspace.create()

    with pytest.raises(WorkspaceError):
        workspace.write_file(
            "../outside.txt",
            "malicious content",
        )


def test_workspace_rejects_deep_path_traversal(tmp_path):
    workspace = WorkspaceManager(tmp_path / "project")
    workspace.create()

    with pytest.raises(WorkspaceError):
        workspace.write_file(
            "src/../../outside.txt",
            "malicious content",
        )


def test_workspace_rejects_absolute_path(tmp_path):
    workspace = WorkspaceManager(tmp_path / "project")
    workspace.create()

    with pytest.raises(WorkspaceError):
        workspace.write_file(
            "/tmp/outside.txt",
            "malicious content",
        )


def test_workspace_does_not_write_outside_root(tmp_path):
    workspace_path = tmp_path / "project"
    outside_path = tmp_path / "outside.txt"

    workspace = WorkspaceManager(workspace_path)
    workspace.create()

    with pytest.raises(WorkspaceError):
        workspace.write_file(
            "../outside.txt",
            "should never be written",
        )

    assert not outside_path.exists()