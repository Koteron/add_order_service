from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

class AddOrderItemsDTO(BaseModel):
    order_id: UUID
    item_id: UUID
    quantity: int = Field(gt=0)

class OrderItemDTO(BaseModel):
    item_id: UUID
    name: str
    quantity: int

class OrderDTO(BaseModel):
    order_id: UUID
    order_contents: list[OrderItemDTO]
    created_at: datetime
