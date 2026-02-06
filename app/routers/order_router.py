from uuid import UUID
from fastapi import APIRouter, Depends, Response, status

from app.services.order_service import get_order_service, OrderService
from app.schemas.order_dtos import AddOrderItemsDTO, OrderDTO
from app.schemas.error_response import ErrorResponse

order_router = APIRouter()

@order_router.get('/all', responses={
})
async def get_orders(
    service: OrderService = Depends(get_order_service)
    ) -> list[OrderDTO]:
    return await service.get_all_orders()

@order_router.get('/{order_id}', responses={
    404: {"model": ErrorResponse, "description": "Not Found"}
})
async def get_order(
    order_id: UUID,
    service: OrderService = Depends(get_order_service)
    ) -> OrderDTO:
    return await service.get_order(order_id)

@order_router.post("", responses={
    403: {"model": ErrorResponse, "description": "Forbidden"},
    404: {"model": ErrorResponse, "description": "Not Found"}
})
async def add_item_to_order(
    dto: AddOrderItemsDTO,
    service: OrderService = Depends(get_order_service)
    ):
    await service.add_item_to_order(dto)
    return Response(status_code=status.HTTP_200_OK)
