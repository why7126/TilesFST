from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.models import Brand
from app.schemas.schemas import BrandCreate, BrandUpdate, BrandResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/brands", tags=["brands"])


@router.get("", response_model=List[BrandResponse])
async def list_brands(db: Session = Depends(get_db)):
    brands = db.query(Brand).order_by(Brand.name).all()
    return brands


@router.get("/{brand_id}", response_model=BrandResponse)
async def get_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand


@router.post("", response_model=BrandResponse)
async def create_brand(
    brand: BrandCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_brand = Brand(**brand.model_dump())
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand


@router.put("/{brand_id}", response_model=BrandResponse)
async def update_brand(
    brand_id: int,
    brand: BrandUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    for key, value in brand.model_dump(exclude_unset=True).items():
        setattr(db_brand, key, value)
    
    db.commit()
    db.refresh(db_brand)
    return db_brand


@router.delete("/{brand_id}")
async def delete_brand(
    brand_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    db.delete(db_brand)
    db.commit()
    return {"message": "Brand deleted successfully"}