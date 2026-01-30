from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.insurance import (
    InsuranceSchema,
    InsuranceCreateSchema,
    InsuranceUpdateSchema
)
from cruds.insurance import get, get_all, create, update, delete
from models.user import UserModel
from core.dependencies import get_current_user, require_permission


router = APIRouter(prefix='/insurance', tags=['insurance'])

@router.get('/', response_model=List[InsuranceSchema])
def read_all(
    db: Session = Depends(get_db),
):
    return get_all(db)

@router.get('/{id}', response_model=InsuranceSchema)
def read_item(
    id: int,
    db: Session = Depends(get_db),
):
    db_obj = get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return db_obj

@router.post('/', response_model=InsuranceSchema)
def create_item(
    item_in: InsuranceCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return create(db, item_in, current_user.id)

@router.put('/{id}', response_model=InsuranceSchema)
def update_item(
    id: int,
    item_in: InsuranceUpdateSchema,
    db: Session = Depends(get_db),
):
    db_obj = get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return update(db, db_obj, item_in)

@router.delete('/{id}')
def delete_item(
    id: int,
    db: Session = Depends(get_db),
):
    db_obj = get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    delete(db, db_obj)
    return {'ok': True}
