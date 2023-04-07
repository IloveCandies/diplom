from fastapi import APIRouter
from mock_data import *
from shemas import *

university_router = APIRouter()

@university_router.post("/university/create/")
async def create(item: University) -> University:
    return item

@university_router.patch("/university/update/")
async def update(item: University):
    return item

@university_router.delete("/university/delete/")
async def delete(item: University) -> University:
    return item
