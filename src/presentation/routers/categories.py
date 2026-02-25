from fastapi import APIRouter, Depends, HTTPException

from src.di.providers import get_create_category_uc, get_list_categories_uc
from src.schemas.categories import CategoryCreate, CategoryRead

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryRead)
async def create(data: CategoryCreate, uc=Depends(get_create_category_uc)):
    try:
        return await uc(
            name=data.name,
            type_=data.type.value if hasattr(data.type, "value") else data.type,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[CategoryRead])
async def list_categories(uc=Depends(get_list_categories_uc)):
    return await uc()