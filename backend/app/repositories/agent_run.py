from uuid import UUID

from sqlalchemy.orm import Session

from backend.app.agent.run import AgentRun
from backend.app.models.agent_run import AgentRunModel

class AgentRunRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, run: AgentRun) -> AgentRunModel:
        model = AgentRunModel(
            id=run.id,
            project_id=run.project_id,
            prompt=run.prompt,
            state=run.state.value,
            plan=run.plan,
            created_at=run.created_at,
            updated_at=run.updated_at
        )

        self.db.add(model)
        self.db.flush()  # Flush to assign an ID to the model before committing
        self.db.refresh(model)

        return model
    
    def get(self, run_id: UUID) -> AgentRunModel | None:
        return (
            self.db.query(AgentRunModel)
            .filter(AgentRunModel.id == run_id)
            .first()
        )
    
    def update(self, run: AgentRun) -> AgentRunModel | None:
        model = self.get(run.id)

        if not model:
            return None

        model.state = run.state.value
        model.plan = run.plan
        model.updated_at = run.updated_at

        self.db.flush()  # Flush to update the model before committing
        self.db.refresh(model)

        return model