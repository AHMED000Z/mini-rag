from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from models.fields import PyObjectId


class Project(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_encoders={
            PyObjectId: lambda x: str(x)
        }
    )

    id: Optional[PyObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)

    @field_validator('project_id')
    @classmethod
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError("project_id must be alphanumeric")
        return value
