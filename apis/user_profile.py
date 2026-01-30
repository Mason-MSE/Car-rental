from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.user_profile import UserProfileSchema,UserProfileCreateSchema,UserProfileUpdateSchema
from cruds.user_profile import get, get_all, create, update, delete
from core.dependencies import get_current_user
from models.user import UserModel

router = APIRouter(prefix='/user_profile', tags=['user_profile'])

@router.get('/', response_model=List[UserProfileSchema])
def read_all(db: Session = Depends(get_db)):
    return get_all(db)

@router.get('/{profile_id}', response_model=UserProfileSchema)
def read_item(profile_id, db: Session = Depends(get_db)):
    db_obj = get(db, profile_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return db_obj

@router.post('/', response_model=UserProfileSchema)
def create_item(item_in: UserProfileCreateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    item_in.user_id=current_user.id
    return create(db, item_in)

@router.put('/{profile_id}', response_model=UserProfileSchema)
def update_item(profile_id, item_in: UserProfileUpdateSchema, db: Session = Depends(get_db)):
    db_obj = get(db, profile_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return update(db, db_obj, item_in)

@router.delete('/{profile_id}')
def delete_item(profile_id, db: Session = Depends(get_db)):
    db_obj = get(db, profile_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    delete(db, db_obj)
    return {'ok': True}
