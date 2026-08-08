from uuid import UUID

from sqlalchemy.orm import Session
from backend.app.models.project import ProjectModel

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str) -> ProjectModel:
        project = ProjectModel(name=name)

        self.db.add(project)
        self.db.flush()  # Flush to assign an ID to the project before committing
        self.db.refresh(project)
        
        return project

    def get(self, project_id: UUID) -> ProjectModel | None:
        return self.db.query(ProjectModel).filter(ProjectModel.id == project_id).first()