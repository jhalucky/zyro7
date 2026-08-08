from backend.app.agent.state import AgentState

def test_Agent_states():
    assert AgentState.CREATED.value == "created"
    assert AgentState.PLANNING.value == "planning"
    assert AgentState.PLANNED.value == "planned"