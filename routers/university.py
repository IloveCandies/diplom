from fastapi import APIRouter
from mock_data import *
from shemas import *

router = APIRouter()

@router.post("/university/create/")
async def create(item: University) -> University:
    return item

@router.patch("/university/update/")
async def update(item: University):
    return item

@router.delete("/university/delete/")
async def delete(item: University) -> University:
    return item
