import sys
from pathlib import Path

from backend.app.agent.run import AgentRun
from backend.app.agent.service import AgentService
from backend.app.agent.runtime import AgentRuntime

from backend.app.core.database import SessionLocal

from backend.app.execution.verifier import BuildVerifier
from backend.app.generation.generator import ProjectGenerator

from backend.app.model.ollama import OllamaProvider

from backend.app.planning.analyzer import RequirementAnalyzer
from backend.app.planning.pipeline import PlanningPipeline
from backend.app.planning.planner import Planner
from backend.app.planning.validator import PlanValidator

from backend.app.repositories.agent_run import AgentRunRepository
from backend.app.repositories.project import ProjectRepository

from backend.app.workspace.manager import WorkspaceManager
from backend.app.execution.installer import DependencyInstaller


PROJECTS_ROOT = Path.home() / "ai-vibe-projects"


def main() -> int:
    if len(sys.argv) < 2:
        print(
            'Usage: python -m scripts.run_agent '
            '"your requirement"'
        )
        return 1

    prompt = " ".join(sys.argv[1:]).strip()

    if not prompt:
        print("Error: prompt cannot be empty.")
        return 1

    db = SessionLocal()

    try:
        # --------------------------------------------------
        # 1. Model
        # --------------------------------------------------

        model = OllamaProvider()

        # --------------------------------------------------
        # 2. Planning pipeline
        # --------------------------------------------------

        analyzer = RequirementAnalyzer(model)
        planner = Planner(model)
        validator = PlanValidator()

        planning_pipeline = PlanningPipeline(
            analyzer=analyzer,
            planner=planner,
            validator=validator,
        )

        # --------------------------------------------------
        # 3. Create project
        # --------------------------------------------------

        project_repository = ProjectRepository(db)

        project = project_repository.create(
            name="Generated Project"
        )

        # --------------------------------------------------
        # 4. Create workspace
        # --------------------------------------------------

        workspace_path = (
            PROJECTS_ROOT / str(project.id)
        )

        workspace = WorkspaceManager(workspace_path)
        workspace.create()

        # --------------------------------------------------
        # 5. Generation + verification
        # --------------------------------------------------

        project_generator = ProjectGenerator(
            workspace
        )

        dependency_installer = DependencyInstaller(
            workspace_path
        )

        build_verifier = BuildVerifier(
            workspace_path
        )

        # --------------------------------------------------
        # 6. Agent repository
        # --------------------------------------------------

        run_repository = AgentRunRepository(db)

        # --------------------------------------------------
        # 7. Runtime
        # --------------------------------------------------

        runtime = AgentRuntime(
            planning_pipeline=planning_pipeline,
            run_repository=run_repository,
            project_generator=project_generator,
            build_verifier=build_verifier,
            dependency_installer=dependency_installer
        )

        # --------------------------------------------------
        # 8. Service
        # --------------------------------------------------

        service = AgentService(runtime)

        # --------------------------------------------------
        # 9. Create AgentRun
        # --------------------------------------------------

        run = AgentRun(
            prompt=prompt,
            project_id=project.id,
        )

        run_repository.create(run)

        # --------------------------------------------------
        # 10. Execute agent
        # --------------------------------------------------

        run = service.execute(run)

        # --------------------------------------------------
        # 11. Commit database changes
        # --------------------------------------------------

        db.commit()

        # --------------------------------------------------
        # 12. Display result
        # --------------------------------------------------

        print()
        print("=" * 70)
        print("AI VIBE PLATFORM")
        print("=" * 70)

        print(f"Prompt: {prompt}")
        print(f"Status: {run.state.value}")
        print(f"Project ID: {project.id}")
        print(f"Workspace: {workspace_path}")

        if run.plan:
            print()
            print("PLAN")
            print("-" * 70)
            print(f"Name: {run.plan.get('name')}")
            print(f"Framework: {run.plan.get('framework')}")
            print(
                f"Package Manager: "
                f"{run.plan.get('package_manager')}"
            )

        if run.verification:
            print()
            print("VERIFICATION")
            print("-" * 70)
            print(
                f"Success: "
                f"{run.verification.get('success')}"
            )
            print(
                f"Exit Code: "
                f"{run.verification.get('exit_code')}"
            )

            if run.verification.get("stdout"):
                print()
                print("Build Output:")
                print(run.verification["stdout"])

            if run.verification.get("stderr"):
                print()
                print("Build Errors:")
                print(run.verification["stderr"])

        print()
        print("=" * 70)

        return 0

    except Exception as exc:
        db.rollback()

        print()
        print("=" * 70)
        print("AGENT FAILED")
        print("=" * 70)
        print(str(exc))
        print("=" * 70)

        return 1

    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())