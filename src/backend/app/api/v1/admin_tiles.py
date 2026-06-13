from fastapi import APIRouter
from app.schemas.tile import TileCreate, TileDetail

router = APIRouter()

@router.post("", response_model=TileDetail)
def create_tile(payload: TileCreate) -> TileDetail:
    return TileDetail(id=1, name=payload.name, model=payload.model, category=payload.category, images=[])
