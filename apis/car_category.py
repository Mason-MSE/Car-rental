from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from core.dependencies import require_permission
from models.user import UserModel
from schemas.car_category import CarCategorySchema,CarCategoryCreateSchema,CarCategoryUpdateSchema
from cruds.car_category import get, get_all, create, update, delete

router = APIRouter(prefix='/car_category', tags=['car_category'])

@router.get('/', response_model=List[CarCategorySchema])
def read_all(db: Session = Depends(get_db)):
    return get_all(db)

@router.get('/{id}', response_model=CarCategorySchema)
def read_item(id, db: Session = Depends(get_db)):
    db_obj = get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return db_obj

@router.post('/', response_model=CarCategorySchema)
def create_item(item_in: CarCategoryCreateSchema, db: Session = Depends(get_db),current_user: UserModel = Depends(require_permission())):
    return create(db, item_in)

@router.put('/{id}', response_model=CarCategorySchema)
def update_item(id, item_in: CarCategoryUpdateSchema, db: Session = Depends(get_db),current_user: UserModel = Depends(require_permission())):
    db_obj = get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return update(db, db_obj, item_in)

@router.delete('/{id}')
def delete_item(id, db: Session = Depends(get_db),current_user: UserModel = Depends(require_permission())):
    db_obj = get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    delete(db, db_obj)
    return {'ok': True}
