from pydantic import BaseModel, Field


class ApplicationPlan(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)

    application_type: str = Field(min_length=1)
    framework: str = Field(min_length=1)
    package_manager: str = Field(min_length=1)

    features: list[str] = Field(default_factory=list)
    pages: list[str] = Field(default_factory=list)
    tasks: list[str] = Field(default_factory=list)