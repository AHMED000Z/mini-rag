from pydantic import BaseModel, Field, validator
from typing import Optional
from models.fields import PyObjectId


class Project(BaseModel):
    _id: Optional[PyObjectId]
    project_id: str = Field(..., min_length=1,)

    @validator('project_id')
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError("project_id must be alphanumeric")

        return value

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True,
        "json_encoders": {
            PyObjectId: lambda x: str(x)
        }
    }
