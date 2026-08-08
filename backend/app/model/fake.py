from .base import ModelProvider

class FakeModelProvider(ModelProvider):
    def generate(self, prompt: str) -> str:
        return f"Fake response for prompt: {prompt}"