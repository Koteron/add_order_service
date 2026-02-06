from fastapi import APIRouter, Depends

from app.services.random_item_data_service import get_item_service, ItemService
from app.schemas.item_dtos import ItemDTO

item_router = APIRouter()

@item_router.post("/generate")
async def generate_random_items(
    count: int = 10,
    service: ItemService = Depends(get_item_service)
) -> list[ItemDTO]:
    return await service.seed_items(item_count=count)

@item_router.get("/all")
async def get_items(
    service: ItemService = Depends(get_item_service)
) -> list[ItemDTO]:
    return await service.get_all_items()
