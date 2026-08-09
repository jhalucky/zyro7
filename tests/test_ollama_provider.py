import httpx

from backend.app.model.ollama import OllamaProvider
from backend.app.model.types import Message, ModelRequest


def test_ollama_provider_generates_response(monkeypatch):
    def mock_post(*args, **kwargs):
        request = httpx.Request(
            "POST",
            "http://localhost:11434/api/chat",
        )

        return httpx.Response(
            200,
            json={
                "model": "qwen2.5-coder:3b",
                "message": {
                    "role": "assistant",
                    "content": "Hello from Ollama!",
                },
                "done": True,
                "done_reason": "stop",
                "prompt_eval_count": 10,
                "eval_count": 5,
                "prompt_eval_duration": 1000,
                "eval_duration": 2000,
            },
            request=request,
        )

    monkeypatch.setattr(httpx, "post", mock_post)

    provider = OllamaProvider()

    request = ModelRequest(
        messages=[
            Message(
                role="user",
                content="Hello, Ollama!",
            )
        ]
    )

    response = provider.generate(request)

    assert response.content == "Hello from Ollama!"
    assert response.finish_reason == "stop"
    assert response.usage["prompt_tokens"] == 10
    assert response.usage["completion_tokens"] == 5