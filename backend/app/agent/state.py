from enum import Enum


class AgentState(str, Enum):
    CREATED = "created"
    PLANNING = "planning"
    PLANNED = "planned"
    GENERATING = "generating"
    GENERATED = "generated"
    VERIFYING = "verifying"
    VERIFIED = "verified"
    FAILED = "failed"