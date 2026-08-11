from pathlib import Path
import pytest
import json

from backend.app.generation.generator import ProjectGenerator
from backend.app.planning.plan import ApplicationPlan
from backend.app.workspace.manager import WorkspaceManager


def test_generator_creates_react_project(tmp_path):
    workspace = WorkspaceManager(tmp_path / "project")
    workspace.create()

    plan = ApplicationPlan(
        name="Coffee Shop",
        description="A coffee shop landing page.",
        application_type="Web Application",
        framework="React",
        package_manager="npm",
        requirements=[
            "Create a modern coffee shop landing page."
        ],
        assumptions=[],
        features=[
            "Hero section",
            "Menu section",
        ],
        pages=[
            "Landing Page",
        ],
        tasks=[
            "Create React application",
        ],
    )

    generator = ProjectGenerator(workspace)

    generator.generate(plan)

    assert workspace.exists("package.json")
    assert workspace.exists("README.md")
    assert workspace.exists("src/App.jsx")


def test_generator_creates_nextjs_project(tmp_path):
    workspace = WorkspaceManager(tmp_path / "project")
    workspace.create()

    plan = ApplicationPlan(
        name="Portfolio",
        description="A portfolio website.",
        application_type="Web Application",
        framework="Next.js",
        package_manager="npm",
        requirements=[
            "Create a portfolio website using Next.js."
        ],
        assumptions=[],
        features=[
            "Projects section",
        ],
        pages=[
            "Home",
            "Projects",
        ],
        tasks=[
            "Create portfolio",
        ],
    )

    generator = ProjectGenerator(workspace)

    generator.generate(plan)

    assert workspace.exists("package.json")
    assert workspace.exists("README.md")
    assert workspace.exists("app/page.tsx")
    assert workspace.exists("app/layout.tsx")

def test_generator_rejects_unsupported_framework(tmp_path):
    workspace = WorkspaceManager(tmp_path / "project")
    workspace.create()

    plan = ApplicationPlan(
        name="Example",
        description="Example application.",
        application_type="Web Application",
        framework="Angular",
        package_manager="npm",
    )

    generator = ProjectGenerator(workspace)

    with pytest.raises(ValueError):
        generator.generate(plan)


import json


def test_react_package_json_is_valid(tmp_path):
    workspace = WorkspaceManager(tmp_path / "project")
    workspace.create()

    plan = ApplicationPlan(
        name="Coffee Shop",
        description="A coffee shop landing page.",
        application_type="Web Application",
        framework="React",
        package_manager="npm",
    )

    generator = ProjectGenerator(workspace)
    generator.generate(plan)

    package_json = json.loads(
        workspace.read_file("package.json")
    )

    assert package_json["name"] == "coffee-shop"
    assert package_json["private"] is True
    assert package_json["dependencies"]["react"] == "latest"
    assert package_json["dependencies"]["react-dom"] == "latest"
    assert package_json["devDependencies"]["vite"] == "latest"


def test_nextjs_package_json_is_valid(tmp_path):
    workspace = WorkspaceManager(tmp_path / "project")
    workspace.create()

    plan = ApplicationPlan(
        name="My Portfolio",
        description="A portfolio website.",
        application_type="Web Application",
        framework="Next.js",
        package_manager="npm",
    )

    generator = ProjectGenerator(workspace)
    generator.generate(plan)

    package_json = json.loads(
        workspace.read_file("package.json")
    )

    assert package_json["name"] == "my-portfolio"
    assert package_json["private"] is True
    assert package_json["dependencies"]["next"] == "latest"
    assert package_json["dependencies"]["react"] == "latest"
    assert package_json["dependencies"]["react-dom"] == "latest"


def test_readme_contains_plan_information(tmp_path):
    workspace = WorkspaceManager(tmp_path / "project")
    workspace.create()

    plan = ApplicationPlan(
        name="Coffee Shop",
        description="A modern coffee shop landing page.",
        application_type="Web Application",
        framework="React",
        package_manager="npm",
    )

    generator = ProjectGenerator(workspace)
    generator.generate(plan)

    readme = workspace.read_file("README.md")

    assert "# Coffee Shop" in readme
    assert "A modern coffee shop landing page." in readme
    assert "React" in readme
    assert "npm" in readme

import json


def test_react_package_json_is_valid(tmp_path):
    workspace = WorkspaceManager(tmp_path / "project")
    workspace.create()

    plan = ApplicationPlan(
        name="Coffee Shop",
        description="A coffee shop landing page.",
        application_type="Web Application",
        framework="React",
        package_manager="npm",
    )

    generator = ProjectGenerator(workspace)
    generator.generate(plan)

    package_json = json.loads(
        workspace.read_file("package.json")
    )

    assert package_json["name"] == "coffee-shop"
    assert package_json["private"] is True
    assert package_json["dependencies"]["react"] == "latest"
    assert package_json["dependencies"]["react-dom"] == "latest"
    assert package_json["devDependencies"]["vite"] == "latest"


def test_nextjs_package_json_is_valid(tmp_path):
    workspace = WorkspaceManager(tmp_path / "project")
    workspace.create()

    plan = ApplicationPlan(
        name="My Portfolio",
        description="A portfolio website.",
        application_type="Web Application",
        framework="Next.js",
        package_manager="npm",
    )

    generator = ProjectGenerator(workspace)
    generator.generate(plan)

    package_json = json.loads(
        workspace.read_file("package.json")
    )

    assert package_json["name"] == "my-portfolio"
    assert package_json["private"] is True
    assert package_json["dependencies"]["next"] == "latest"
    assert package_json["dependencies"]["react"] == "latest"
    assert package_json["dependencies"]["react-dom"] == "latest"


def test_readme_contains_plan_information(tmp_path):
    workspace = WorkspaceManager(tmp_path / "project")
    workspace.create()

    plan = ApplicationPlan(
        name="Coffee Shop",
        description="A modern coffee shop landing page.",
        application_type="Web Application",
        framework="React",
        package_manager="npm",
    )

    generator = ProjectGenerator(workspace)
    generator.generate(plan)

    readme = workspace.read_file("README.md")

    assert "# Coffee Shop" in readme
    assert "A modern coffee shop landing page." in readme
    assert "React" in readme
    assert "npm" in readme

def test_package_name_is_normalized(tmp_path):
    workspace = WorkspaceManager(tmp_path / "project")
    workspace.create()

    plan = ApplicationPlan(
        name="My Awesome Project!",
        description="Test project.",
        application_type="Web Application",
        framework="React",
        package_manager="npm",
    )

    generator = ProjectGenerator(workspace)
    generator.generate(plan)

    package_json = json.loads(
        workspace.read_file("package.json")
    )

    assert package_json["name"] == "my-awesome-project"