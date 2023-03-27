from fastapi import APIRouter
from mock_data import *
from shemas import *

router = APIRouter()
@router.get("/groups/all")
async def get_groups() -> List[Group]: 
    return Groups
