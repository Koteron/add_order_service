from uuid import UUID, uuid4
from typing import TYPE_CHECKING
from sqlalchemy import Index
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy_utils import Ltree, LtreeType

from app.models.base import Base
if TYPE_CHECKING:
    from app.models.item import Item
else:
    Item = "Item"

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    parent_tree: Mapped[Ltree] = mapped_column(LtreeType, nullable=False)
    is_leaf: Mapped[bool]

    items: Mapped[list["Item"]] = relationship("Item", back_populates="category")

    __table_args__ = (
        Index("index_categories_parent_tree_gist", "parent_tree", postgresql_using="gist"),
    )