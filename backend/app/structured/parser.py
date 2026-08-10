import json
import re
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from backend.app.structured.errors import StructuredOutputError


T = TypeVar("T", bound=BaseModel)


class StructuredOutputParser:
    def parse(
        self,
        content: str,
        schema: type[T],
    ) -> T:
        json_content = self._extract_json(content)

        try:
            data = json.loads(json_content)
        except json.JSONDecodeError as exc:
            raise StructuredOutputError(
                "Model response contains invalid JSON."
            ) from exc

        try:
            return schema.model_validate(data)
        except ValidationError as exc:
            raise StructuredOutputError(
                f"Model response failed schema validation: {exc}"
            ) from exc

    @staticmethod
    def _extract_json(content: str) -> str:
        content = content.strip()

        if content.startswith("```"):
            match = re.search(
                r"```(?:json)?\s*(.*?)\s*```",
                content,
                re.DOTALL | re.IGNORECASE,
            )

            if not match:
                raise StructuredOutputError(
                    "Could not extract JSON from code fence."
                )

            content = match.group(1).strip()

        return content