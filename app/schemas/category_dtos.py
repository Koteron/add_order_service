from uuid import UUID
from pydantic import BaseModel

class CategoryDTO(BaseModel):
    id: UUID
    name: str
    parent_tree: str