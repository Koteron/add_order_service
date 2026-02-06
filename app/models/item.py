from uuid import UUID, uuid4
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.models.base import Base
from app.models.category import Category
if TYPE_CHECKING:
    from app.models.order_item import OrderItem
else:
    OrderItem = "OrderItem"

class Item(Base):
    __tablename__ = "items"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    quantity: Mapped[int]
    price: Mapped[float]
    category_id: Mapped[UUID] = mapped_column(ForeignKey("categories.id"))

    category: Mapped["Category"] = relationship("Category", back_populates="items")
    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="item")
