import json

from backend.app.planning.plan import ApplicationPlan
from backend.app.workspace.manager import WorkspaceManager


class ProjectGenerator:
    def __init__(self, workspace: WorkspaceManager):
        self.workspace = workspace

    def generate(self, plan: ApplicationPlan) -> None:
        framework = plan.framework.lower()

        if framework in {"react", "react.js"}:
            self._generate_react(plan)
            return

        if framework in {"next.js", "nextjs"}:
            self._generate_nextjs(plan)
            return

        raise ValueError(
            f"Unsupported framework: {plan.framework}"
        )

    def _generate_react(self, plan: ApplicationPlan) -> None:
        self.workspace.write_file(
            "package.json",
            json.dumps(
                {
                    "name": self._package_name(plan.name),
                    "private": True,
                    "version": "0.1.0",
                    "type": "module",
                    "scripts": {
                        "dev": "vite",
                        "build": "vite build",
                    },
                    "dependencies": {
                        "react": "latest",
                        "react-dom": "latest",
                    },
                    "devDependencies": {
                        "vite": "latest",
                    },
                },
                indent=2,
            )
            + "\n",
        )

        self.workspace.write_file(
            "README.md",
            self._readme(plan),
        )

        self.workspace.write_file(
            "src/App.jsx",
            """export default function App() {
  return (
    <main>
      <h1>Application</h1>
    </main>
  );
}
""",
        )

    def _generate_nextjs(self, plan: ApplicationPlan) -> None:
        self.workspace.write_file(
            "package.json",
            json.dumps(
                {
                    "name": self._package_name(plan.name),
                    "private": True,
                    "version": "0.1.0",
                    "scripts": {
                        "dev": "next dev",
                        "build": "next build",
                        "start": "next start",
                    },
                    "dependencies": {
                        "next": "latest",
                        "react": "latest",
                        "react-dom": "latest",
                    },
                },
                indent=2,
            )
            + "\n",
        )

        self.workspace.write_file(
            "README.md",
            self._readme(plan),
        )

        self.workspace.write_file(
            "app/layout.tsx",
            """import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Application",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
""",
        )

        self.workspace.write_file(
            "app/page.tsx",
            """export default function Home() {
  return (
    <main>
      <h1>Application</h1>
    </main>
  );
}
""",
        )

    @staticmethod
    def _package_name(name: str) -> str:
        value = name.lower().strip()
        value = "".join(
            char if char.isalnum() else "-"
            for char in value
        )

        value = "-".join(
            part for part in value.split("-") if part
        )

        return value or "generated-project"

    @staticmethod
    def _readme(plan: ApplicationPlan) -> str:
        return f"""# {plan.name}

{plan.description}

## Framework

{plan.framework}

## Package Manager

{plan.package_manager}
"""