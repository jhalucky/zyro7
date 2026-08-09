from enum import Enum

from pydantic import BaseModel, Field


class AnalysisStatus(str, Enum):
    READY = "ready"
    NEEDS_CLARIFICATION = "needs_clarification"


class RequirementAnalysis(BaseModel):
    status: AnalysisStatus

    summary: str = Field(min_length=1)

    constraints: list[str] = Field(default_factory=list)

    questions: list[str] = Field(default_factory=list)