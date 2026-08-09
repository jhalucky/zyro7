from .base import ModelProvider
from .types import ModelRequest, ModelResponse


class FakeModelProvider(ModelProvider):

    def generate(self, request: ModelRequest) -> ModelResponse:
        user_message = next(
            message
            for message in reversed(request.messages)
            if message.role == "user"
        )

        return ModelResponse(
            content=f"Fake response for: {user_message.content}"
        )