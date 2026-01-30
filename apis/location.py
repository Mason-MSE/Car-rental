from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.location import LocationSchema,LocationCreateSchema,LocationUpdateSchema
from cruds.location import get, get_all, create, update, delete

router = APIRouter(prefix='/location', tags=['location'])

@router.get('/', response_model=List[LocationSchema])
def read_all(db: Session = Depends(get_db)):
    return get_all(db)

@router.get('/{id}', response_model=LocationSchema)
def read_item(id, db: Session = Depends(get_db)):
    db_obj = get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return db_obj

@router.post('/', response_model=LocationSchema)
def create_item(item_in: LocationCreateSchema, db: Session = Depends(get_db)):
    return create(db, item_in)

@router.post('/batch_create', response_model=List[LocationSchema])
def create_items(items: List[LocationCreateSchema], db: Session = Depends(get_db)):
    return [create(db, item_in) for item_in in items]

@router.put('/{id}', response_model=LocationSchema)
def update_item(id, item_in: LocationUpdateSchema, db: Session = Depends(get_db)):
    db_obj = get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return update(db, db_obj, item_in)

@router.delete('/{id}')
def delete_item(id, db: Session = Depends(get_db)):
    db_obj = get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    delete(db, db_obj)
    return {'ok': True}
