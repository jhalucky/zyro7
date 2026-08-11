from pathlib import Path


class WorkspaceError(Exception):
    """Raised when a workspace operation is invalid."""


class WorkspaceManager:
    def __init__(self, root: Path):
        self.root = Path(root).resolve()

    def create(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)

    def write_file(self, relative_path: str, content: str) -> Path:
        path = self._resolve_path(relative_path)

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

        return path

    def read_file(self, relative_path: str) -> str:
        path = self._resolve_path(relative_path)

        if not path.exists():
            raise WorkspaceError(
                f"File does not exist: {relative_path}"
            )

        if not path.is_file():
            raise WorkspaceError(
                f"Path is not a file: {relative_path}"
            )

        return path.read_text(encoding="utf-8")

    def exists(self, relative_path: str) -> bool:
        path = self._resolve_path(relative_path)
        return path.exists()

    def _resolve_path(self, relative_path: str) -> Path:
        path = Path(relative_path)

        if path.is_absolute():
            raise WorkspaceError(
                "Absolute paths are not allowed."
            )

        resolved = (self.root / path).resolve()

        try:
            resolved.relative_to(self.root)
        except ValueError as exc:
            raise WorkspaceError(
                f"Path escapes workspace: {relative_path}"
            ) from exc

        return resolved