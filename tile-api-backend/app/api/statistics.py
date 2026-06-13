from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import get_db
from app.models.models import Statistic, StatTypeEnum
from app.schemas.schemas import StatisticsSummary
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("/summary", response_model=StatisticsSummary)
async def get_statistics_summary(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    views = db.query(func.sum(Statistic.count)).filter(Statistic.type == StatTypeEnum.VIEW).scalar() or 0
    favorites = db.query(func.sum(Statistic.count)).filter(Statistic.type == StatTypeEnum.FAVORITE).scalar() or 0
    shares = db.query(func.sum(Statistic.count)).filter(Statistic.type == StatTypeEnum.SHARE).scalar() or 0
    
    return StatisticsSummary(
        total_views=views,
        total_favorites=favorites,
        total_shares=shares
    )


@router.post("/report")
async def report_statistic(
    product_id: int,
    stat_type: StatTypeEnum,
    db: Session = Depends(get_db)
):
    stat = db.query(Statistic).filter(
        Statistic.product_id == product_id,
        Statistic.type == stat_type
    ).first()
    
    if stat:
        stat.count += 1
    else:
        stat = Statistic(product_id=product_id, type=stat_type, count=1)
        db.add(stat)
    
    db.commit()
    return {"message": "Statistic reported"}


@router.get("/product/{product_id}")
async def get_product_statistics(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    stats = db.query(Statistic).filter(Statistic.product_id == product_id).all()
    return stats