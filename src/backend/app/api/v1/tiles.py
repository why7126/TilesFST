from fastapi import APIRouter
from app.schemas.tile import TileDetail, TileListItem

router = APIRouter()

@router.get(
    "",
    response_model=list[TileListItem],
    summary="获取瓷砖列表",
)
def list_tiles() -> list[TileListItem]:
    return []

@router.get(
    "/{tile_id}",
    response_model=TileDetail,
    summary="获取瓷砖详情",
)
def get_tile(tile_id: int) -> TileDetail:
    return TileDetail(id=tile_id, name="示例瓷砖", model="MODEL-001", category="通体砖", images=[])
