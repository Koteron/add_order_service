from uuid import UUID
from pydantic import BaseModel

from app.schemas.category_dtos import CategoryDTO

class ItemDTO(BaseModel):
    id: UUID
    name: str
    quantity: int
    price: float
    category: CategoryDTO
