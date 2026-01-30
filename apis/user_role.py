from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.user_role import UserRoleSchema,UserRoleCreateSchema,UserRoleUpdateSchema
from cruds.user_role import get, get_all, create, update, delete

router = APIRouter(prefix='/user_role', tags=['user_role'])

@router.get('/', response_model=List[UserRoleSchema])
def read_all(db: Session = Depends(get_db)):
    return get_all(db)

@router.get('/{user_id}/{role_id}', response_model=UserRoleSchema)
def read_item(user_id, role_id, db: Session = Depends(get_db)):
    db_obj = get(db, user_id, role_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return db_obj

@router.post('/', response_model=UserRoleSchema)
def create_item(item_in: UserRoleCreateSchema, db: Session = Depends(get_db)):
    return create(db, item_in)

@router.put('/{user_id}/{role_id}', response_model=UserRoleSchema)
def update_item(user_id, role_id, item_in: UserRoleUpdateSchema, db: Session = Depends(get_db)):
    db_obj = get(db, user_id, role_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return update(db, db_obj, item_in)

@router.delete('/{user_id}/{role_id}')
def delete_item(user_id, role_id, db: Session = Depends(get_db)):
    db_obj = get(db, user_id, role_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    delete(db, db_obj)
    return {'ok': True}
