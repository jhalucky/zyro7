import httpx

from backend.app.model.ollama import OllamaProvider


def test_ollama_provider_generates_response(monkeypatch):
    def mock_post(*args, **kwargs):
        request = httpx.Request(
            "POST",
            "http://localhost:11434/api/generate",
        )

        return httpx.Response(
            200,
            json={
                "response": "Hello from Ollama!",
            },
            request=request,
        )

    monkeypatch.setattr(httpx, "post", mock_post)

    provider = OllamaProvider()

    response = provider.generate("Hello, Ollama!")

    assert response == "Hello from Ollama!"