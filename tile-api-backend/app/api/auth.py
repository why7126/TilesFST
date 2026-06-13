from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.models import Employee
from app.schemas.schemas import LoginRequest, TokenResponse
from app.services.auth_service import verify_password, create_access_token, get_current_user
from app.core.logging import logger

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.username == request.username).first()
    if not employee or not verify_password(request.password, employee.password_hash):
        logger.warning(f"Login failed for username: {request.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    token_data = {
        "sub": str(employee.id),
        "username": employee.username,
        "role": employee.role.value
    }
    access_token = create_access_token(token_data)
    logger.info(f"User logged in: {employee.username}")
    
    return TokenResponse(access_token=access_token)


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user