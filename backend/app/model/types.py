from dataclasses import dataclass, field
from typing import Any, Literal

MessageRole = Literal["system","user","assistant","tool"]

@dataclass(frozen=True)
class Message:
    role: MessageRole
    content: str

@dataclass(frozen=True)
class ModelRequest:
    messages: list[Message]
    temperature: float = 0.2
    max_tokens: int | None = None
    response_format: str = "text"

@dataclass(frozen=True)
class ModelResponse:
    content: str
    finish_reason: str | None = None
    usage: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    
