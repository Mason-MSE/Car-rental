# routers/insurance_company.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.insurance import (
    InsuranceCompanySchema,
    InsuranceCompanyCreateSchema,
    InsuranceCompanyUpdateSchema
)
from cruds.insurance_company import get, get_all, create, update, delete
from models.user import UserModel
from core.dependencies import get_current_user, require_permission

router = APIRouter(prefix="/insurance_company", tags=["insurance_company"])

@router.get("/", response_model=List[InsuranceCompanySchema])
def read_all(db: Session = Depends(get_db)):
    return get_all(db)

@router.get("/{id}", response_model=InsuranceCompanySchema)
def read_item(id: int, db: Session = Depends(get_db)):
    db_obj = get(db, id)
    if not db_obj:
        raise HTTPException(404, "Item not found")
    return db_obj

@router.post("/", response_model=InsuranceCompanySchema)
def create_item(item_in: InsuranceCompanyCreateSchema, db: Session = Depends(get_db),current_user: UserModel = Depends(require_permission())):
    return create(db, item_in)

@router.put("/{id}", response_model=InsuranceCompanySchema)
def update_item(id: int, item_in: InsuranceCompanyUpdateSchema, db: Session = Depends(get_db),current_user: UserModel = Depends(require_permission())):
    db_obj = get(db, id)
    if not db_obj:
        raise HTTPException(404, "Item not found")
    return update(db, db_obj, item_in)

@router.delete("/{id}")
def delete_item(id: int, db: Session = Depends(get_db),current_user: UserModel = Depends(require_permission())):
    db_obj = get(db, id)
    if not db_obj:
        raise HTTPException(404, "Item not found")
    delete(db, db_obj)
    return {"ok": True}
