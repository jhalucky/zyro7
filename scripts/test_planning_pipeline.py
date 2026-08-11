from backend.app.model.ollama import OllamaProvider
from backend.app.planning.analyzer import RequirementAnalyzer
from backend.app.planning.pipeline import PlanningPipeline
from backend.app.planning.planner import Planner
from backend.app.planning.validator import PlanValidator


def main():
    model = OllamaProvider()

    analyzer = RequirementAnalyzer(model)
    planner = Planner(model)
    validator = PlanValidator()

    pipeline = PlanningPipeline(
        analyzer=analyzer,
        planner=planner,
        validator=validator,
    )

    requirements = [
        "Create a modern landing page for a coffee shop.",
        "Create a portfolio website using Next.js and Tailwind CSS.",
        "Build me something for a coffee shop.",
    ]

    for requirement in requirements:
        print("\n" + "=" * 70)
        print("REQUIREMENT:")
        print(requirement)
        print("=" * 70)

        result = pipeline.run(requirement)

        print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()