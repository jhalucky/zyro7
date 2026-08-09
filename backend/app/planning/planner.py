import json

from backend.app.model.base import ModelProvider
from backend.app.model.types import Message, ModelRequest
from backend.app.planning.plan import PlanningResult
from backend.app.planning.prompts import (
    PLANNER_SYSTEM_PROMPT,
    build_planner_prompt,
)


class Planner:
    def __init__(self, model: ModelProvider):
        self.model = model

    def create_plan(self, requirement: str) -> PlanningResult:
        if not requirement.strip():
            raise ValueError("Requirement cannot be empty.")

        request = ModelRequest(
            messages=[
                Message(
                    role="system",
                    content=PLANNER_SYSTEM_PROMPT,
                ),
                Message(
                    role="user",
                    content=build_planner_prompt(requirement),
                ),
            ],
            temperature=0.2,
        )

        response = self.model.generate(request)

        data = json.loads(response.content)

        return PlanningResult.model_validate(data)