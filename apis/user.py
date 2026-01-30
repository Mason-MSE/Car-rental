from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from core.dependencies import get_current_user, oauth2_scheme
from schemas.user import UserSchema,UserCreateSchema,UserUpdateSchema
from cruds.user import get, get_all, create, soft_delete, update, delete

router = APIRouter(prefix='/user', tags=['user'])

@router.get('/', response_model=List[UserSchema])
def read_all(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    return get_all(db)

@router.get('/{id}', response_model=UserSchema)
def read_item(id, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_obj = get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return db_obj

@router.post('/', response_model=UserSchema)
def create_item(item_in: UserCreateSchema, db: Session = Depends(get_db)):
    return create(db, item_in)

@router.put('/{id}', response_model=UserSchema)
def update_item(id, item_in: UserUpdateSchema, db: Session = Depends(get_db)):
    db_obj = get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return update(db, db_obj, item_in)

@router.delete('/{id}')
def delete_item(id, db: Session = Depends(get_db)):
    db_obj = get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    soft_delete(db, db_obj)
    return {'ok': True}
