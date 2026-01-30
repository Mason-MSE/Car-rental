from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from core.dependencies import require_permission
from models.user import UserModel
from schemas.car import CarSchema,CarCreateSchema,CarUpdateSchema
from cruds.car import get, get_all, create, update, delete

router = APIRouter(prefix='/car', tags=['car'])

@router.get('/', response_model=List[CarSchema])
def read_all(db: Session = Depends(get_db)):
    return get_all(db)

@router.get('/{car_id}', response_model=CarSchema)
def read_item(car_id, db: Session = Depends(get_db)):
    db_obj = get(db, car_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return db_obj

@router.post('/', response_model=CarSchema)
def create_item(item_in: CarCreateSchema, db: Session = Depends(get_db),current_user: UserModel = Depends(require_permission())):
    return create(db, item_in)

@router.post('/batch_create', response_model=List[CarSchema])
def create_items(items: List[CarCreateSchema], db: Session = Depends(get_db),current_user: UserModel = Depends(require_permission())):
    return [create(db, item_in) for item_in in items]

@router.put('/{car_id}', response_model=CarSchema)
def update_item(car_id, item_in: CarUpdateSchema, db: Session = Depends(get_db),current_user: UserModel = Depends(require_permission())):
    db_obj = get(db, car_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return update(db, db_obj, item_in)

@router.delete('/{car_id}' ,response_model=None)
def delete_item(car_id, db: Session = Depends(get_db),current_user: UserModel = Depends(require_permission())):
    db_obj = get(db, car_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    delete(db, db_obj)
    return {'ok': True}

