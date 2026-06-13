from fastapi import APIRouter, Depends
from app.core.deps import require_admin_access
from app.schemas.tile import TileCreate, TileDetail

router = APIRouter(dependencies=[Depends(require_admin_access)])

@router.post(
    "",
    response_model=TileDetail,
    summary="创建瓷砖",
    tags=["admin-tiles"],
)
def create_tile(payload: TileCreate) -> TileDetail:
    return TileDetail(id=1, name=payload.name, model=payload.model, category=payload.category, images=[])
