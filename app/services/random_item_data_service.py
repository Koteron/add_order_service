import random
import string

from uuid import uuid4
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import Ltree

from app.models.category import Category
from app.models.item import Item
from app.config.db import get_async_session
from app.schemas.item_dtos import ItemDTO
from app.schemas.category_dtos import CategoryDTO


def get_item_service(session: AsyncSession = Depends(get_async_session)):
    return ItemService(session)

class ItemService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def seed_items(self, item_count: int = 10):
        result = await self.session.execute(
            select(Category).limit(1)
        )
        category = result.scalar_one_or_none()

        if not category:
            category = Category(
                id=uuid4(),
                name=self._random_name(),
                parent_tree=Ltree("category.subcategory.leaf_category"),
                is_leaf=True
            )
            self.session.add(category)
            await self.session.commit()
            await self.session.refresh(category)

        items = []
        for _ in range(item_count):
            item = Item(
                name=self._random_name(),
                quantity=random.randint(1, 100),
                price=round(random.uniform(1.0, 100.0), 2),
                category_id=category.id
            )
            items.append(item)

        self.session.add_all(items)
        await self.session.commit()
        return [ 
            ItemDTO(
                id=item.id,
                name=item.name,
                quantity=item.quantity,
                price=item.price,
                category=CategoryDTO(
                    id=category.id,
                    name=category.name,
                    parent_tree=category.parent_tree.path,
                    is_leaf=category.is_leaf
                )
            )
            for item in items
        ]
    
    async def get_all_items(self):
        result = await self.session.execute(
            select(Item)
            .options(
                joinedload(Item.category)
            )
        )
        items = result.scalars().all()
        return [ 
            ItemDTO(
                id=item.id,
                name=item.name,
                quantity=item.quantity,
                price=item.price,
                category=CategoryDTO(
                    id=item.category.id,
                    name=item.category.name,
                    parent_tree=item.category.parent_tree.path,
                    is_leaf=item.category.is_leaf
                )
            )
            for item in items
        ]

    def _random_name(self, length: int = 8) -> str:
        return "".join(random.choices(string.ascii_letters, k=length))
