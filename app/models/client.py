from uuid import UUID, uuid4
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.models.base import Base
if TYPE_CHECKING:
    from app.models.order import Order
else:
    Order = "Order"

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    address: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    client_orders: Mapped["Order"] = relationship("Order", back_populates="client")
