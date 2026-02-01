from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from core.dependencies import get_current_user, require_permission
from models.user import UserModel
from schemas.insurance import InsuranceCreateSchema
from schemas.rent_fee import RentFeeCreateSchema, RentFeeUpdateSchema
from schemas.car import CarUpdateSchema
from schemas.booking import BookingApprovalSchema, BookingReturnCarSchema, BookingSchema,BookingCreateSchema,BookingUpdateSchema
from cruds.booking import get, get_all, create, update, delete
import cruds.car as car_crud
import cruds.rent_fee as rent_fee_crud
import cruds.driver_license as driver_license_crud  
import cruds.user_profile as user_profile_crud
import cruds.insurance_catalogue as insurance_catalogue_crud
import cruds.insurance_company as insurance_company_crud
import cruds.insurance_price as insurance_price_crud
import cruds.insurance as insurance_crud
import services.bookingservice as boooking_service



router = APIRouter(prefix='/booking', tags=['booking'])

@router.get('/', response_model=List[BookingSchema])
def read_all(db: Session = Depends(get_db)):
    return get_all(db)

@router.get('/{booking_id}', response_model=BookingSchema)
def read_item(booking_id, db: Session = Depends(get_db)):
    db_obj = get(db, booking_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return db_obj



@router.post('/', response_model=BookingSchema)
def create_item(item_in: BookingCreateSchema, db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    return boooking_service.create_item(item_in,db,current_user)

@router.put('/{booking_id}', response_model=BookingSchema)
def update_item(booking_id, item_in: BookingUpdateSchema, db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    return boooking_service.update_item(booking_id,item_in,db)

@router.delete('/{booking_id}')
def delete_item(booking_id, db: Session = Depends(get_db)):
    db_obj = get(db, booking_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    delete(db, db_obj)
    return {'ok': True}

@router.put('/approval/{booking_id}')
def approval(booking_id,item_in: BookingApprovalSchema, db: Session = Depends(get_db),user=Depends(require_permission())):
    return boooking_service.approval(booking_id,item_in,db)

@router.put('/return/{booking_id}')
def return_car( item_in: BookingReturnCarSchema,db: Session = Depends(get_db)):
    return boooking_service.return_car(item_in,db)