from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.resource import ResourceSchema,ResourceCreateSchema,ResourceUpdateSchema
from cruds.resource import get, get_all, create, update, delete

router = APIRouter(prefix='/resource', tags=['resource'])

@router.get('/', response_model=List[ResourceSchema])
def read_all(db: Session = Depends(get_db)):
    return get_all(db)

@router.get('/{id}', response_model=ResourceSchema)
def read_item(id, db: Session = Depends(get_db)):
    db_obj = get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return db_obj

@router.post('/', response_model=ResourceSchema)
def create_item(item_in: ResourceCreateSchema, db: Session = Depends(get_db)):
    return create(db, item_in)

@router.put('/{id}', response_model=ResourceSchema)
def update_item(id, item_in: ResourceUpdateSchema, db: Session = Depends(get_db)):
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
