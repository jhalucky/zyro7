import pytest
from backend.app.model.base import ModelProvider
from backend.app.model.types import ModelRequest, ModelResponse
from backend.app.planning.analysis import AnalysisStatus
from backend.app.planning.analyzer import RequirementAnalyzer
from backend.app.structured.errors import StructuredOutputError


class ReadyAnalyzerModel(ModelProvider):
    def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            content="""
            {
                "status": "ready",
                "summary": "A coffee shop landing page.",
                "constraints": [],
                "questions": []
            }
            """
        )


def test_analyzer_detects_ready_requirement():
    analyzer = RequirementAnalyzer(ReadyAnalyzerModel())

    result = analyzer.analyze(
        "Create a landing page for a coffee shop."
    )

    assert result.status == AnalysisStatus.READY
    assert result.summary == "A coffee shop landing page."
    assert result.questions == []



class ClarificationAnalyzerModel(ModelProvider):
    def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            content="""
            {
                "status": "needs_clarification",
                "summary": "The requested coffee shop application is ambiguous.",
                "constraints": [],
                "questions": [
                    "What type of application would you like to build?"
                ]
            }
            """
        )


def test_analyzer_detects_ambiguous_requirement():
    analyzer = RequirementAnalyzer(ClarificationAnalyzerModel())

    result = analyzer.analyze(
        "Build me something for a coffee shop."
    )

    assert result.status == AnalysisStatus.NEEDS_CLARIFICATION
    assert result.questions
    assert result.questions[0] == (
        "What type of application would you like to build?"
    )


class InvalidAnalyzerModel(ModelProvider):
    def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            content="This is not valid JSON."
        )


def test_analyzer_rejects_invalid_json():
    analyzer = RequirementAnalyzer(InvalidAnalyzerModel())

    with pytest.raises(StructuredOutputError):
        analyzer.analyze(
            "Create a portfolio website."
        )

def test_analyzer_rejects_empty_requirement():
    analyzer = RequirementAnalyzer(ReadyAnalyzerModel())

    with pytest.raises(ValueError):
        analyzer.analyze("")

class ClearLandingPageModel(ModelProvider):
    def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            content="""
            {
                "status": "ready",
                "summary": "A modern landing page for a coffee shop.",
                "constraints": [],
                "questions": []
            }
            """
        )


def test_analyzer_accepts_clear_but_underspecified_requirement():
    analyzer = RequirementAnalyzer(ClearLandingPageModel())

    result = analyzer.analyze(
        "Create a modern landing page for a coffee shop."
    )

    assert result.status == AnalysisStatus.READY
    assert result.questions == []

class ConstraintAnalyzerModel(ModelProvider):
    def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            content="""
            {
                "status": "ready",
                "summary": "A portfolio website.",
                "constraints": [
                    "Next.js",
                    "Tailwind CSS"
                ],
                "questions": []
            }
            """
        )

def test_analyzer_extracts_constraints():
    analyzer = RequirementAnalyzer(ConstraintAnalyzerModel())

    result = analyzer.analyze(
        "Create a portfolio using Next.js and Tailwind CSS."
    )

    assert result.status == AnalysisStatus.READY
    assert "Next.js" in result.constraints
    assert "Tailwind CSS" in result.constraints