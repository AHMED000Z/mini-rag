from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from models.fields import PyObjectId


class DataChunk(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_encoders={
            PyObjectId: lambda x: str(x)
        }
    )

    id: Optional[PyObjectId] = Field(None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: PyObjectId
    chunk_asset_id: PyObjectId

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [
                    ("chunk_project_id", 1)  # 1 is for ascending
                ],
                "name": "chunk_project_id_index_1",
                "unique": False
            }
        ]
