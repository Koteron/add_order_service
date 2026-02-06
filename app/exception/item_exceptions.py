from typing import Optional
from uuid import UUID
from app.exception.http_exceptions import NotFoundException, ForbiddenException

class ItemNotFoundException(NotFoundException):
    def __init__(self, item_id: UUID):
        self.item_id = item_id
        super().__init__(f"Item with id=({item_id}) not found")

class InsufficientItemQuantityException(ForbiddenException):
    def __init__(
        self,
        item_id: UUID,
        requested_quantity: int,
        available_quantity: int,
        item_name: Optional[str] = None
    ):
        self.item_id = item_id
        self.requested_quantity = requested_quantity
        self.available_quantity = available_quantity

        if item_name:
            self.item_name = item_name
        else:
            self.item_name = "item"
        
        super().__init__((
            f"Cannot create order for '{self.item_name}' (ID: {item_id}). "
            f"Requested: {requested_quantity}, Available: {available_quantity}"
        )  )