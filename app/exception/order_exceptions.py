from uuid import UUID
from app.exception.http_exceptions import NotFoundException

class OrderNotFoundException(NotFoundException):
    def __init__(self, order_id: UUID):
        self.order_id = order_id
        super().__init__(f"Order with id=({order_id}) not found")
