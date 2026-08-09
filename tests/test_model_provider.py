from backend.app.model.fake import FakeModelProvider
from backend.app.model.types import Message, ModelRequest


def test_fake_model_provider():
    model = FakeModelProvider()

    request = ModelRequest(
        messages=[
            Message(
                role="user",
                content="Hello",
            )
        ]
    )

    response = model.generate(request)

    assert response.content == "Fake response for: Hello"