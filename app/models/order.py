from uuid import UUID, uuid4
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Index, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.models.base import Base
if TYPE_CHECKING:
    from app.models.client import Client
    from app.models.order_item import OrderItem
else:
    Client = "Client"
    OrderItem = "OrderItem"

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    client_id: Mapped[UUID] = mapped_column(ForeignKey("clients.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")
    client: Mapped["Client"] = relationship("Client", back_populates="client_orders")

    __table_args__ = (
        Index("index_client_order_created_at", "created_at"),
    )