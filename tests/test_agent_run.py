import pytest

from backend.app.agent.run import AgentRun
from backend.app.agent.state import AgentState


def test_agent_run_starts_in_created_state():
    run = AgentRun(prompt="Create a coffee shop landing page")

    assert run.state == AgentState.CREATED


def test_valid_state_transitions():
    run = AgentRun(prompt="Create a coffee shop landing page")

    run.transition_to(AgentState.PLANNING)

    assert run.state == AgentState.PLANNING

    run.transition_to(AgentState.PLANNED)

    assert run.state == AgentState.PLANNED


def test_invalid_state_transition_is_rejected():
    run = AgentRun(prompt="Create a coffee shop landing page")

    with pytest.raises(ValueError):
        run.transition_to(AgentState.PLANNED)


def test_completed_state_cannot_be_reached_yet():
    run = AgentRun(prompt="Create a coffee shop landing page")

    run.transition_to(AgentState.PLANNING)
    run.transition_to(AgentState.PLANNED)

    with pytest.raises(ValueError):
        run.transition_to(AgentState.CREATED)

def test_run_can_transition_through_generation():
    run = AgentRun(
        prompt="Create a coffee shop landing page"
    )

    run.transition_to(AgentState.PLANNING)
    run.transition_to(AgentState.PLANNED)
    run.transition_to(AgentState.GENERATING)
    run.transition_to(AgentState.GENERATED)

    assert run.state == AgentState.GENERATED