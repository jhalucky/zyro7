from backend.app.model.fake import FakeModelProvider

def test_fake_model_provider():
    model = FakeModelProvider()

    response = model.generate("Test prompt")

    assert response == "Fake response for prompt: Test prompt"