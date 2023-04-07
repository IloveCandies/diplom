from fastapi import APIRouter
from mock_data import *
from shemas import *

oop_router = APIRouter()

@oop_router.post("/oop/create/")
async def create(item: University) -> OOP:
    return item

@oop_router.patch("/oop/update/")
async def update(item: University):
    return item

@oop_router.delete("/university/delete/")
async def delete(item: University) -> OOP:
    return item
