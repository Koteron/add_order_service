from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.config.db import get_async_session
from app.schemas.order_dtos import OrderDTO, OrderItemDTO, AddOrderItemsDTO
from app.models.order import Order
from app.models.item import Item
from app.models.order_item import OrderItem
from app.scripts.create_test_client import create_or_get_test_client
from app.exception.order_exceptions import OrderNotFoundException
from app.exception.item_exceptions import InsufficientItemQuantityException, ItemNotFoundException

def get_order_service(session: AsyncSession = Depends(get_async_session)):
    return OrderService(session)

class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_order(self, order_id: UUID) -> OrderDTO:
        result_order = await self.session.execute(select(Order).where(
            Order.id == order_id
        ))
        order = result_order.scalar_one_or_none()

        if not order:
            raise OrderNotFoundException(order_id=order_id)

        result_order_item = await self.session.execute(select(OrderItem).where(
            OrderItem.order_id == order_id
        ).options(joinedload(OrderItem.item)))
        order_items = result_order_item.scalars().all()

        return OrderDTO(
            order_id=order_id,
            order_contents=[
                OrderItemDTO(
                    item_id=order_item.item_id,
                    name=order_item.item.name,
                    quantity=order_item.quantity
                    )
                 for order_item in order_items
                 ],
            created_at=order.created_at
        )
        
    # Should be by client, but I feel like it would require registration, so it's out of scope
    async def get_all_orders(self) -> list[OrderDTO]: 
        result = await self.session.execute(
            select(Order)
            .options(
                joinedload(Order.order_items)
                .joinedload(OrderItem.item)
            )
        )
        orders = result.unique().scalars().all()
        return [
            OrderDTO(
                order_id=order.id,
                order_contents=[
                    OrderItemDTO(
                        item_id=order_item.item.id,
                        name=order_item.item.name,
                        quantity=order_item.quantity
                        )
                    for order_item in order.order_items
                    ],
                created_at=order.created_at
            )
            for order in orders
        ]

    async def add_item_to_order(self, dto: AddOrderItemsDTO) -> None:
        result_item_update = await self.session.execute(
            select(Item)
            .where(Item.id == dto.item_id)
            .with_for_update()
        )

        item = result_item_update.scalar_one_or_none()

        if not item:
            raise ItemNotFoundException(item_id=dto.item_id)
        elif item.quantity < dto.quantity:
            raise InsufficientItemQuantityException(
                item_id=item.id,
                available_quantity=item.quantity,
                requested_quantity=dto.quantity    
            )

        item.quantity -= dto.quantity

        result_order = await self.session.execute(
            select(Order)
            .where(Order.id == dto.order_id)
        )
        order = result_order.scalar_one_or_none()

        if not order:
            order = Order(
                id=dto.order_id, 
                client_id=(await create_or_get_test_client(self.session)).id
            )
            self.session.add(order)
            await self.session.flush()
        
        result_order_item = await self.session.execute(
            select(OrderItem)
            .where(
            OrderItem.order_id == dto.order_id,
            OrderItem.item_id == dto.item_id
            )
            .with_for_update(skip_locked=True))
        order_item = result_order_item.scalar_one_or_none()
        
        if not order_item:
            order_item = OrderItem(
                order_id=order.id, 
                item_id=item.id,
                quantity=dto.quantity
            )
            self.session.add(order_item)
        else:
            order_item.quantity += dto.quantity
        
        await self.session.commit()

