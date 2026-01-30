from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.insurance import (
    InsurancePriceSchema,
    InsurancePriceCreateSchema,
    InsurancePriceUpdateSchema
)
from cruds.insurance_price import get, get_all, create, update, delete
from models.user import UserModel
from core.dependencies import get_current_user, require_permission

router = APIRouter(prefix="/insurance_price", tags=["insurance_price"])

@router.get("/", response_model=List[InsurancePriceSchema])
def read_all(db: Session = Depends(get_db)):
    return get_all(db)

@router.get("/{id}", response_model=InsurancePriceSchema)
def read_item(id: int, db: Session = Depends(get_db)):
    db_obj = get(db, id)
    if not db_obj:
        raise HTTPException(404, "Item not found")
    return db_obj

@router.post("/", response_model=InsurancePriceSchema)
def create_item(item_in: InsurancePriceCreateSchema, db: Session = Depends(get_db),current_user: UserModel = Depends(require_permission())):
    
    return create(db, item_in)
@router.post("/batch_create", response_model=List[InsurancePriceSchema])
def create_item(item_in: List[InsurancePriceCreateSchema], db: Session = Depends(get_db),current_user: UserModel = Depends(require_permission())):
    
    return [create(db, item) for item in item_in]

@router.put("/{id}", response_model=InsurancePriceSchema)
def update_item(id: int, item_in: InsurancePriceUpdateSchema, db: Session = Depends(get_db),current_user: UserModel = Depends(require_permission())):
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
