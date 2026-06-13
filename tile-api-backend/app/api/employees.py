from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.models import Employee
from app.schemas.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.services.auth_service import get_current_user
from app.services.permissions import require_admin
from app.services.auth_service import get_password_hash

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("", response_model=List[EmployeeResponse])
async def list_employees(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    require_admin(current_user)
    employees = db.query(Employee).all()
    return employees


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    require_admin(current_user)
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.post("", response_model=EmployeeResponse)
async def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    require_admin(current_user)
    
    existing = db.query(Employee).filter(Employee.username == employee.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    db_employee = Employee(
        username=employee.username,
        password_hash=get_password_hash(employee.password),
        role=employee.role
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    require_admin(current_user)
    
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if employee.role:
        db_employee.role = employee.role
    if employee.password:
        db_employee.password_hash = get_password_hash(employee.password)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    require_admin(current_user)
    
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_employee)
    db.commit()
    return {"message": "Employee deleted successfully"}


@router.post("/{employee_id}/reset-password")
async def reset_password(
    employee_id: int,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    require_admin(current_user)
    
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db_employee.password_hash = get_password_hash(new_password)
    db.commit()
    return {"message": "Password reset successfully"}