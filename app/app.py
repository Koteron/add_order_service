from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config.db import verify_schema
from app.routers.order_router import order_router
from app.routers.item_router import item_router
from app.exception.global_handler import register_global_exception_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    await verify_schema()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(order_router, prefix='/orders', tags=["orders"])
app.include_router(item_router, prefix='/items', tags=["item"])

register_global_exception_handler(app)