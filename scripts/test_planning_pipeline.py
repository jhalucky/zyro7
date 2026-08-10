from backend.app.model.ollama import OllamaProvider
from backend.app.planning.analyzer import RequirementAnalyzer
from backend.app.planning.pipeline import PlanningPipeline
from backend.app.planning.planner import Planner


def main():
    model = OllamaProvider()

    analyzer = RequirementAnalyzer(model)
    planner = Planner(model)

    pipeline = PlanningPipeline(
        analyzer=analyzer,
        planner=planner,
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