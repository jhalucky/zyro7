from backend.app.agent.state import AgentState

def test_Agent_states():
    assert AgentState.CREATED.value == "created"
    assert AgentState.PLANNING.value == "planning"
    assert AgentState.PLANNED.value == "planned"

def test_agent_can_transition_to_generating():
    assert AgentState.GENERATING.value == "generating"


def test_agent_can_transition_to_generated():
    assert AgentState.GENERATED.value == "generated"

    