import pytest
from pydantic import BaseModel

from backend.app.structured.errors import StructuredOutputError
from backend.app.structured.parser import StructuredOutputParser


class ExampleOutput(BaseModel):
    name: str
    count: int

def test_parser_accepts_valid_json():
    parser = StructuredOutputParser()

    result = parser.parse(
        '{"name": "test", "count": 5}',
        ExampleOutput,
    )

    assert result.name == "test"
    assert result.count == 5


def test_parser_accepts_whitespace():
    parser = StructuredOutputParser()

    result = parser.parse(
        """
        {
            "name": "test",
            "count": 5
        }
        """,
        ExampleOutput,
    )

    assert result.name == "test"
    assert result.count == 5


def test_parser_extracts_json_from_code_fence():
    parser = StructuredOutputParser()

    result = parser.parse(
        """
        ```json
        {
            "name": "test",
            "count": 5
        }
        ```
        """,
        ExampleOutput,
    )

    assert result.name == "test"
    assert result.count == 5


def test_parser_extracts_json_from_plain_code_fence():
    parser = StructuredOutputParser()

    result = parser.parse(
        """
        ```
        {
            "name": "test",
            "count": 5
        }
        ```
        """,
        ExampleOutput,
    )

    assert result.name == "test"
    assert result.count == 5


def test_parser_rejects_invalid_json():
    parser = StructuredOutputParser()

    try:
        parser.parse(
            "This is not JSON.",
            ExampleOutput,
        )

        assert False, "Expected StructuredOutputError"
    except StructuredOutputError as exc:
        assert "invalid JSON" in str(exc)


def test_parser_rejects_invalid_json():
    parser = StructuredOutputParser()

    with pytest.raises(StructuredOutputError, match="invalid JSON"):
        parser.parse(
            "This is not JSON.",
            ExampleOutput,
        )

def test_parser_rejects_schema_validation_failure():
    parser = StructuredOutputParser()

    with pytest.raises(
        StructuredOutputError,
        match="schema validation",
    ):
        parser.parse(
            '{"name": "test"}',
            ExampleOutput,
        )


def test_parser_rejects_malformed_code_fence():
    parser = StructuredOutputParser()

    with pytest.raises(
        StructuredOutputError,
        match="Could not extract JSON",
    ):
        parser.parse(
            "```json\n{\"name\": \"test\", \"count\": 5}",
            ExampleOutput,
        )



        