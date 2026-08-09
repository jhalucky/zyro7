import json

from backend.app.model.base import ModelProvider
from backend.app.model.types import Message, ModelRequest
from backend.app.planning.analysis import RequirementAnalysis
from backend.app.planning.analyzer_prompts import (
    ANALYZER_SYSTEM_PROMPT,
    build_analyzer_prompt,
)


class RequirementAnalyzer:
    def __init__(self, model: ModelProvider):
        self.model = model

    def analyze(self, requirement: str) -> RequirementAnalysis:
        if not requirement.strip():
            raise ValueError("Requirement cannot be empty.")

        request = ModelRequest(
            messages=[
                Message(
                    role="system",
                    content=ANALYZER_SYSTEM_PROMPT,
                ),
                Message(
                    role="user",
                    content=build_analyzer_prompt(requirement),
                ),
            ],
            temperature=0.0,
        )

        response = self.model.generate(request)

        data = json.loads(response.content)

        return RequirementAnalysis.model_validate(data)