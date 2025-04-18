from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "示例项目",
                "description": "这是一个示例项目描述"
            }
        } 