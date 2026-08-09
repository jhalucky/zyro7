from abc import ABC, abstractmethod
from .types import ModelRequest, ModelResponse

class ModelProvider(ABC):

    @abstractmethod
    def generate(self, request: ModelRequest) -> ModelResponse:
        raise NotImplementedError