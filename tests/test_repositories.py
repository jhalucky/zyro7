from backend.app.agent.run import AgentRun
from backend.app.agent.state import AgentState
from backend.app.core.database import SessionLocal
from backend.app.repositories.agent_run import AgentRunRepository
from backend.app.repositories.project import ProjectRepository


def test_create_and_get_project(db):

    try:
        repository = ProjectRepository(db)

        project = repository.create("Test Project")

        retrieved = repository.get(project.id)

        assert retrieved is not None
        assert retrieved.id == project.id
        assert retrieved.name == "Test Project"

    finally:
        db.close()


def test_create_and_get_agent_run(db):
    

    try:
        project_repository = ProjectRepository(db)
        run_repository = AgentRunRepository(db)

        project = project_repository.create("Agent Test Project")

        run = AgentRun(
            prompt="Create a coffee shop landing page",
            project_id=project.id,
        )

        saved = run_repository.create(run)
        retrieved = run_repository.get(run.id)

        assert retrieved is not None
        assert retrieved.id == run.id
        assert retrieved.project_id == project.id
        assert retrieved.prompt == run.prompt
        assert retrieved.state == AgentState.CREATED.value

    finally:
        db.close()


def test_agent_run_state_persists(db):
    # db = SessionLocal()

    try:
        project_repository = ProjectRepository(db)
        run_repository = AgentRunRepository(db)

        project = project_repository.create("State Test Project")

        run = AgentRun(
            prompt="Create an application",
            project_id=project.id,
        )

        run_repository.create(run)

        run.transition_to(AgentState.PLANNING)

        updated = run_repository.update(run)

        assert updated is not None
        assert updated.state == AgentState.PLANNING.value

        retrieved = run_repository.get(run.id)

        assert retrieved is not None
        assert retrieved.state == AgentState.PLANNING.value

    finally:
        db.close()


