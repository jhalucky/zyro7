from backend.app.planning.analysis import (
    AnalysisStatus,
    RequirementAnalysis,
)
from backend.app.planning.pipeline import PlanningPipeline
from backend.app.planning.plan import (
    ApplicationPlan,
    PlanningResult,
    PlanningStatus,
)


class FakeAnalyzer:
    def __init__(self, result):
        self.result = result
        self.called = False

    def analyze(self, requirement):
        self.called = True
        return self.result


class FakePlanner:
    def __init__(self, result):
        self.result = result
        self.called = False

    def create_plan(self, analysis):
        self.called = True
        return self.result


def test_pipeline_returns_clarification_without_planning():
    analysis = RequirementAnalysis(
        status=AnalysisStatus.NEEDS_CLARIFICATION,
        summary="A coffee shop application.",
        questions=[
            "What type of application do you want?"
        ],
    )

    analyzer = FakeAnalyzer(analysis)

    planner_result = PlanningResult(
        status=PlanningStatus.READY,
        plan=ApplicationPlan(
            name="Should Not Be Created",
            description="Should not be created.",
            application_type="web",
            framework="React",
            package_manager="npm",
        ),
    )

    planner = FakePlanner(planner_result)

    pipeline = PlanningPipeline(analyzer, planner)

    result = pipeline.run(
        "Build me something for a coffee shop."
    )

    assert result.status == AnalysisStatus.NEEDS_CLARIFICATION
    assert result.questions == [
        "What type of application do you want?"
    ]

    assert analyzer.called is True
    assert planner.called is False



from backend.app.planning.analysis import (
    AnalysisStatus,
    RequirementAnalysis,
)
from backend.app.planning.pipeline import PlanningPipeline
from backend.app.planning.plan import (
    ApplicationPlan,
    PlanningResult,
    PlanningStatus,
)


class FakeAnalyzer:
    def __init__(self, result):
        self.result = result
        self.called = False

    def analyze(self, requirement):
        self.called = True
        return self.result


class FakePlanner:
    def __init__(self, result):
        self.result = result
        self.called = False

    def create_plan(self, analysis):
        self.called = True
        return self.result


def test_pipeline_returns_clarification_without_planning():
    analysis = RequirementAnalysis(
        status=AnalysisStatus.NEEDS_CLARIFICATION,
        summary="A coffee shop application.",
        questions=[
            "What type of application do you want?"
        ],
    )

    analyzer = FakeAnalyzer(analysis)

    planner_result = PlanningResult(
        status=PlanningStatus.READY,
        plan=ApplicationPlan(
            name="Should Not Be Created",
            description="Should not be created.",
            application_type="web",
            framework="React",
            package_manager="npm",
        ),
    )

    planner = FakePlanner(planner_result)

    pipeline = PlanningPipeline(analyzer, planner)

    result = pipeline.run(
        "Build me something for a coffee shop."
    )

    assert result.status == AnalysisStatus.NEEDS_CLARIFICATION
    assert result.questions == [
        "What type of application do you want?"
    ]

    assert analyzer.called is True
    assert planner.called is False


class InspectingPlanner:
    def __init__(self, result):
        self.result = result
        self.analysis = None

    def create_plan(self, analysis):
        self.analysis = analysis
        return self.result
    


def test_pipeline_passes_analysis_to_planner():
    analysis = RequirementAnalysis(
        status=AnalysisStatus.READY,
        summary="A portfolio website.",
        constraints=[
            "Next.js",
            "Tailwind CSS",
        ],
    )

    analyzer = FakeAnalyzer(analysis)

    planner_result = PlanningResult(
        status=PlanningStatus.READY,
        plan=ApplicationPlan(
            name="Portfolio",
            description="A portfolio website.",
            application_type="web",
            framework="Next.js",
            package_manager="npm",
        ),
    )

    planner = InspectingPlanner(planner_result)

    pipeline = PlanningPipeline(analyzer, planner)

    pipeline.run(
        "Create a portfolio using Next.js and Tailwind CSS."
    )

    assert planner.analysis is analysis
    assert "Next.js" in planner.analysis.constraints
    assert "Tailwind CSS" in planner.analysis.constraints