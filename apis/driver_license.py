from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from core.dependencies import get_current_user
from models.user import UserModel
from schemas.driver_license import DriverLicenseSchema,DriverLicenseCreateSchema,DriverLicenseUpdateSchema
from cruds.driver_license import get, get_all, create, update, delete

router = APIRouter(prefix='/driver_license', tags=['driver_license'])

@router.get('/', response_model=List[DriverLicenseSchema])
def read_all(db: Session = Depends(get_db)):
    return get_all(db)

@router.get('/{driver_license_id}', response_model=DriverLicenseSchema)
def read_item(driver_license_id, db: Session = Depends(get_db)):
    db_obj = get(db, driver_license_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return db_obj

@router.post('/', response_model=DriverLicenseSchema)
def create_item(item_in: DriverLicenseCreateSchema, db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    item_in.user_id=current_user.id
    return create(db, item_in)

@router.put('/{driver_license_id}', response_model=DriverLicenseSchema)
def update_item(driver_license_id, item_in: DriverLicenseUpdateSchema, db: Session = Depends(get_db)):
    db_obj = get(db, driver_license_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return update(db, db_obj, item_in)

@router.delete('/{driver_license_id}')
def delete_item(driver_license_id, db: Session = Depends(get_db)):
    db_obj = get(db, driver_license_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    delete(db, db_obj)
    return {'ok': True}
