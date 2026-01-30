from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.role_resource import RoleResourceSchema,RoleResourceCreateSchema,RoleResourceUpdateSchema
from cruds.role_resource import get, get_all, create, update, delete

router = APIRouter(prefix='/role_resource', tags=['role_resource'])

@router.get('/', response_model=List[RoleResourceSchema])
def read_all(db: Session = Depends(get_db)):
    return get_all(db)

@router.get('/{id}', response_model=RoleResourceSchema)
def read_item(id, db: Session = Depends(get_db)):
    db_obj = get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return db_obj

@router.post('/', response_model=RoleResourceSchema)
def create_item(item_in: RoleResourceCreateSchema, db: Session = Depends(get_db)):
    return create(db, item_in)

@router.put('/{id}', response_model=RoleResourceSchema)
def update_item(id, item_in: RoleResourceUpdateSchema, db: Session = Depends(get_db)):
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
