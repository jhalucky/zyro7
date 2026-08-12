from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from .state import AgentState

ALLOWED_TRANSITIONS: dict[AgentState, set[AgentState]] = {
    AgentState.CREATED: {
        AgentState.PLANNING,
    },
    AgentState.PLANNING: {
        AgentState.PLANNED,
    },
    AgentState.PLANNED: {
        AgentState.GENERATING,
    },
    AgentState.GENERATING: {
        AgentState.GENERATED,
        AgentState.FAILED,
    },
    AgentState.GENERATED: {
        AgentState.VERIFYING,
    },
    AgentState.VERIFYING: {
        AgentState.VERIFIED,
        AgentState.FAILED,
    },
    AgentState.VERIFIED: set(),
    AgentState.FAILED: set(),
}

@dataclass
class AgentRun:
    prompt: str
    project_id: UUID | None = None
    
    id: UUID = field(default_factory=uuid4)
    state: AgentState = AgentState.CREATED
    plan: dict[str, Any] | None = None
    verification: dict[str, Any] | None = None

    created_at: datetime = field(
        default_factory=lambda:
datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda:
datetime.now(timezone.utc)
    )

    def transition_to(self, new_state: AgentState) -> None:
        allowed_states = ALLOWED_TRANSITIONS[self.state]

        if new_state not in allowed_states:
            raise ValueError(
                f"Invalid state transition:"
                f"{self.state.value} -> {new_state.value}"
            )

        self.state = new_state
        self.updated_at = datetime.now(timezone.utc)