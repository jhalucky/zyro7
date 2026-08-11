from pydantic import BaseModel, Field
from enum import Enum

class PlanningStatus(str, Enum):
    READY = "ready"
    NEEDS_CLARIFICATION = "needs_clarification"


class ApplicationPlan(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)

    application_type: str = Field(min_length=1)
    framework: str = Field(min_length=1)
    package_manager: str = Field(min_length=1)

    requirements: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)

    features: list[str] = Field(default_factory=list)
    pages: list[str] = Field(default_factory=list)
    tasks: list[str] = Field(default_factory=list)


class PlanningResult(BaseModel):
    status: PlanningStatus
    plan: ApplicationPlan | None = None
    message: str | None = None
    questions: list[str] = Field(default_factory=list)