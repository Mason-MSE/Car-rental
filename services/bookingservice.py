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



def generate_policy_number():
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S") + f"{int(now.microsecond / 1000):03d}"
    policy_number = f"CARRENT_{timestamp}"
    return policy_number


def create_item(item_in, db,current_user):
    user_id=current_user.id
    item_in.user_id=user_id
    driver_license=driver_license_crud.get_by_user_id(db,user_id)
    if not driver_license:
        raise HTTPException(status_code=400, detail='User has no driver license, cannot book car')
    user_profile=user_profile_crud.get_by_user_id(db,user_id)   
    if not user_profile:
        raise HTTPException(status_code=400, detail='User profile is not verified, cannot book car')

    car=car_crud.get(db, item_in.car_id)  # Ensure the car exists
    if not car:
        raise HTTPException(status_code=400, detail='Car does not exist')
    if car.is_available != 1: # Assuming 1 means available            
        raise HTTPException(status_code=400, detail='Car is not available for booking')
  
    bookingmodel=create(db, item_in)

    hours = Decimal(
    (bookingmodel.end_date - bookingmodel.start_date).total_seconds()) / Decimal("3600")
    hourly_rate = Decimal(car.daily_rate) / Decimal("24")
    base_amount = (hourly_rate * hours).quantize(
        Decimal("0.00"),
        rounding=ROUND_HALF_UP
    )

    insurance_price_model=insurance_price_crud.get(db,item_in.insurance_price_id)
    if not insurance_price_model:
        raise  HTTPException(status_code=400, detail='Insurance premium not exist')
    insurance_catalogue_model=insurance_catalogue_crud.get(db,insurance_price_model.catalogue_id)
    if not insurance_price_model:
        raise  HTTPException(status_code=400, detail='Insurance Catalogue not exist')
    insurance_company_model=insurance_company_crud.get(db,insurance_catalogue_model.company_id)
    if not insurance_company_model:
        raise HTTPException(status_code=400, detail='Insurance company not exist')
    insurance_crud.create(db,InsuranceCreateSchema(
                                booking_id=bookingmodel.booking_id,
                                insurance_type=insurance_catalogue_model.insurance_type,
                                policy_number=generate_policy_number(),
                                provider=insurance_company_model.name,
                                insurance_price_id=item_in.insurance_price_id,
                                coverage_amount=insurance_price_model.coverage_amount,
                                premium=insurance_price_model.premium,
                                start_date=bookingmodel.start_date.date(),
                                end_date=bookingmodel.end_date.date()
                                ),current_user.id)

    rent_fee_crud.create(db, RentFeeCreateSchema(
                                                booking_id=bookingmodel.booking_id,
                                                base_amount=base_amount,
                                                insurance_amount=10.0,
                                                tax_amount=round(float(base_amount) * 0.01, 2),
                                                late_fee=0.0,
                                                discount_amount=0.0,
                                                total_amount=round(float(base_amount) + 10.0 + round(float(base_amount) * 0.01, 2),2)   
                                                )) # Create associated rent fee record)
    return bookingmodel



def update_item(booking_id, item_in, db):
    db_obj = get(db, booking_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    car=car_crud.get(db, db_obj.car_id) 
    if not car:
        raise HTTPException(status_code=400, detail='Car does not exist')
    if car.is_available != 1: # Assuming 1 means available            
        raise HTTPException(status_code=400, detail='Car is not available for booking')
    
    print("Updating booking:", db_obj, "with data:", item_in)
    bookingmodel = update(db, db_obj, item_in)
    print("Updated booking:", bookingmodel)
    
    hours = Decimal(
    (bookingmodel.end_date - bookingmodel.start_date).total_seconds()) / Decimal("3600")
    hourly_rate = Decimal(car.daily_rate) / Decimal("24")
    base_amount = (hourly_rate * hours).quantize(
        Decimal("0.00"),
        rounding=ROUND_HALF_UP
    )
    print("hours:", hours, "hours_rate:", hourly_rate, "Calculated base amount:", base_amount)
    rent_fee = rent_fee_crud.get_by_booking_id(db, bookingmodel.booking_id)
    if  not rent_fee:
        rent_fee_crud.create(db, RentFeeCreateSchema(
                                                booking_id=bookingmodel.booking_id,
                                                base_amount=base_amount,
                                                insurance_amount=10.0,
                                                tax_amount=round(float(base_amount) * 0.01, 2),
                                                late_fee=0.0,
                                                discount_amount=0.0,
                                                total_amount=round(float(base_amount) + 10.0 + round(float(base_amount) * 0.01, 2),2)   
                                                )) # Create associated rent fee record)
    else:
        rent_fee_crud.update(db, rent_fee,RentFeeUpdateSchema(
                                                    booking_id=bookingmodel.booking_id,
                                                    base_amount=base_amount,
                                                    insurance_amount=10.0,
                                                    tax_amount=round(float(base_amount) * 0.01, 2),
                                                    late_fee=0.0,
                                                    discount_amount=0.0,
                                                    total_amount=round(float(base_amount) + 10.0 + round(float(base_amount) * 0.01, 2),2) 
                                                    ) ) # update associated rent fee record)

    return bookingmodel

def approval(booking_id,item_in: BookingApprovalSchema, db):
    db_obj = get(db, booking_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    if db_obj.status != 0:
        raise HTTPException(status_code=400, detail='Booking has already been processed')
    if item_in.status==1:
        car_model = car_crud.get(db, db_obj.car_id)  # Mark car as available    
        if not car_model:
            raise HTTPException(status_code=404, detail='Item not found')
        car_crud.update(db, car_model, CarUpdateSchema(is_available=0))  # Mark car as not available
    return update(db, db_obj, item_in)


def return_car( item_in,db):
    db_obj = get(db, item_in.booking_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    car_model = car_crud.get(db, db_obj.car_id)  # Mark car as available    
    if not car_model:
        raise HTTPException(status_code=404, detail='Item not found')
    car_crud.update(db, car_model, CarUpdateSchema(is_available=1,location_id=item_in.drop_location))  # Mark car as available
    current_time=datetime.now()
    if current_time > db_obj.end_date:
        # Calculate late fee
        late_hours = Decimal(
            (current_time - db_obj.end_date).total_seconds()) / Decimal("3600")
        hourly_rate = Decimal(car_model.daily_rate) / Decimal("24")
        late_fee = (hourly_rate * late_hours).quantize(
            Decimal("0.00"),
            rounding=ROUND_HALF_UP
        )
        rent_fee = rent_fee_crud.get_by_booking_id(db, db_obj.booking_id)
        if rent_fee:
            rent_fee_crud.update(db, rent_fee, RentFeeUpdateSchema(
                late_fee=late_fee,
                total_amount=rent_fee.total_amount + float(late_fee)
            ))

    bookingmodel=update(db, db_obj, BookingUpdateSchema(status=2, drop_location=item_in.drop_location, drop_time=current_time))
    return bookingmodel