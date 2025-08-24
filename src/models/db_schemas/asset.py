from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from models.fields import PyObjectId
from datetime import datetime


class Asset(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_encoders={
            PyObjectId: lambda x: str(x)
        }
    )

    id: Optional[PyObjectId] = Field(None, alias="_id")
    asset_project_id: PyObjectId
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1)
    asset_size: int = Field(ge=0, default=None)
    asset_config: dict = Field(default=None)
    asset_pushed_at: datetime = Field(default=datetime.utcnow)

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [
                    ("asset_project_id", 1)  # 1 is for ascending
                ],
                "name": "asset_project_id_index_1",
                "unique": False
            },
            {
                "key": [
                    ("asset_project_id", 1),  # 1 is for ascending
                    ("asset_name", 1)
                ],
                "name": "asset_project_id_name_index_1",
                "unique": True
            }
        ]
