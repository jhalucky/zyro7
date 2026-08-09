import httpx

from .base import ModelProvider
from .types import ModelRequest, ModelResponse


class OllamaProvider(ModelProvider):
    def __init__(
        self,
        model: str = "qwen2.5-coder:3b",
        base_url: str = "http://localhost:11434",
        timeout: float = 120.0,
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(self, request: ModelRequest) -> ModelResponse:
        response = httpx.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": message.role,
                        "content": message.content,
                    }
                    for message in request.messages
                ],
                "stream": False,
                "options": {
                    "temperature": request.temperature,
                },
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        message = data["message"]

        return ModelResponse(
            content=message["content"],
            finish_reason=data.get("done_reason"),
            usage={
                "prompt_tokens": data.get("prompt_eval_count", 0),
                "completion_tokens": data.get("eval_count", 0),
                "prompt_eval_duration_ns": data.get(
                    "prompt_eval_duration", 0
                ),
                "completion_eval_duration_ns": data.get(
                    "eval_duration", 0
                ),
            },
            metadata={
                "model": data.get("model"),
                "created_at": data.get("created_at"),
            },
        )