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

# -------------------------
# Observer Pattern Classes
# -------------------------
class Observer:
    """Observer interface. Any class that wants to be notified about booking events should implement this interface."""
    def notify(self, booking, event_type: str):
        raise NotImplementedError

class EmailNotifier(Observer):
    """Simulate sending email notification when a booking event occurs."""
    def notify(self, booking, event_type: str):
        print(f"[EMAIL] Booking {booking.booking_id} has event: {event_type}")

class PushNotifier(Observer):
    """Simulate sending push notification when a booking event occurs."""
    def notify(self, booking, event_type: str):
        print(f"[PUSH] Booking {booking.booking_id} has event: {event_type}")

class BookingSubject:
    """Subject class for the Observer Pattern.
    Maintains a list of observers and notifies them on booking events.
    """
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        """Add an observer to the list."""
        self._observers.append(observer)

    def detach(self, observer: Observer):
        """Remove an observer from the list."""
        self._observers.remove(observer)

    def notify_observers(self, booking, event_type: str):
        """Notify all observers about a booking event."""
        for observer in self._observers:
            observer.notify(booking, event_type)

# Global booking subject instance
booking_subject = BookingSubject()
booking_subject.attach(EmailNotifier())  # Attach email notifier
booking_subject.attach(PushNotifier())   # Attach push notifier


def generate_policy_number():
    """Generate a unique policy number using timestamp and microseconds."""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S") + f"{int(now.microsecond / 1000):03d}"
    policy_number = f"CARRENT_{timestamp}"
    return policy_number


def create_item(item_in, db,current_user):
    """Create a new booking, associated insurance and rent fee, and notify observers."""
    
    user_id=current_user.id
    item_in.user_id=user_id

    # Check if user has a valid driver license
    driver_license=driver_license_crud.get_by_user_id(db,user_id)
    if not driver_license:
        raise HTTPException(status_code=400, detail='User has no driver license, cannot book car')

    # Check if user profile is verified
    user_profile=user_profile_crud.get_by_user_id(db,user_id)   
    if not user_profile:
        raise HTTPException(status_code=400, detail='User profile is not verified, cannot book car')

    # Check if car exists and is available
    car=car_crud.get(db, item_in.car_id)
    if not car:
        raise HTTPException(status_code=400, detail='Car does not exist')
    if car.is_available != 1:         
        raise HTTPException(status_code=400, detail='Car is not available for booking')
  
    # Create booking record
    bookingmodel=create(db, item_in)

    # Calculate base rent amount based on hours and hourly rate
    hours = Decimal((bookingmodel.end_date - bookingmodel.start_date).total_seconds()) / Decimal("3600")
    hourly_rate = Decimal(car.daily_rate) / Decimal("24")
    base_amount = (hourly_rate * hours).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

    # Fetch insurance price and catalogue
    insurance_price_model=insurance_price_crud.get(db,item_in.insurance_price_id)
    if not insurance_price_model:
        raise  HTTPException(status_code=400, detail='Insurance premium not exist')
    insurance_catalogue_model=insurance_catalogue_crud.get(db,insurance_price_model.catalogue_id)
    if not insurance_price_model:
        raise  HTTPException(status_code=400, detail='Insurance Catalogue not exist')
    insurance_company_model=insurance_company_crud.get(db,insurance_catalogue_model.company_id)
    if not insurance_company_model:
        raise HTTPException(status_code=400, detail='Insurance company not exist')

    # Create insurance record
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

    # Create rent fee record
    rent_fee_crud.create(db, RentFeeCreateSchema(
        booking_id=bookingmodel.booking_id,
        base_amount=base_amount,
        insurance_amount=10.0,
        tax_amount=round(float(base_amount) * 0.01, 2),
        late_fee=0.0,
        discount_amount=0.0,
        total_amount=round(float(base_amount) + 10.0 + round(float(base_amount) * 0.01, 2),2)
    ))

    # Notify observers about new booking creation
    booking_subject.notify_observers(bookingmodel, "created")
    return bookingmodel



def update_item(booking_id, item_in, db):
    """Update a booking record and its rent fee, then notify observers."""
    
    db_obj = get(db, booking_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')

    # Check if car exists and is available
    car=car_crud.get(db, db_obj.car_id) 
    if not car:
        raise HTTPException(status_code=400, detail='Car does not exist')
    if car.is_available != 1:         
        raise HTTPException(status_code=400, detail='Car is not available for booking')
    
    print("Updating booking:", db_obj, "with data:", item_in)
    bookingmodel = update(db, db_obj, item_in)
    print("Updated booking:", bookingmodel)
    
    # Calculate updated base rent amount
    hours = Decimal((bookingmodel.end_date - bookingmodel.start_date).total_seconds()) / Decimal("3600")
    hourly_rate = Decimal(car.daily_rate) / Decimal("24")
    base_amount = (hourly_rate * hours).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
    print("hours:", hours, "hours_rate:", hourly_rate, "Calculated base amount:", base_amount)

    # Update or create rent fee record
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
        ))
    else:
        rent_fee_crud.update(db, rent_fee,RentFeeUpdateSchema(
            booking_id=bookingmodel.booking_id,
            base_amount=base_amount,
            insurance_amount=10.0,
            tax_amount=round(float(base_amount) * 0.01, 2),
            late_fee=0.0,
            discount_amount=0.0,
            total_amount=round(float(base_amount) + 10.0 + round(float(base_amount) * 0.01, 2),2)
        ))

    # Notify observers about booking update
    booking_subject.notify_observers(bookingmodel, "updated")
    return bookingmodel

def approval(booking_id,item_in: BookingApprovalSchema, db):
    """Approve or reject a booking and notify observers."""
    
    db_obj = get(db, booking_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    if db_obj.status != 0:
        raise HTTPException(status_code=400, detail='Booking has already been processed')

    # Mark car as unavailable if booking approved
    if item_in.status==1:
        car_model = car_crud.get(db, db_obj.car_id)    
        if not car_model:
            raise HTTPException(status_code=404, detail='Item not found')
        car_crud.update(db, car_model, CarUpdateSchema(is_available=0))

    bookingmodel = update(db, db_obj, item_in)

    # Notify observers about booking approval or rejection
    event_type = "approved" if item_in.status == 1 else "rejected"
    booking_subject.notify_observers(bookingmodel, event_type)
    return bookingmodel


def return_car( item_in,db):
    """Process car return, calculate late fees if any, and notify observers."""
    
    db_obj = get(db, item_in.booking_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')

    # Mark car as available at drop-off location
    car_model = car_crud.get(db, db_obj.car_id)    
    if not car_model:
        raise HTTPException(status_code=404, detail='Item not found')
    car_crud.update(db, car_model, CarUpdateSchema(is_available=1,location_id=item_in.drop_location))

    current_time=datetime.now()

    # Calculate late fee if car returned after booking end date
    if current_time > db_obj.end_date:
        late_hours = Decimal((current_time - db_obj.end_date).total_seconds()) / Decimal("3600")
        hourly_rate = Decimal(car_model.daily_rate) / Decimal("24")
        late_fee = (hourly_rate * late_hours).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

        rent_fee = rent_fee_crud.get_by_booking_id(db, db_obj.booking_id)
        if rent_fee:
            rent_fee_crud.update(db, rent_fee, RentFeeUpdateSchema(
                late_fee=late_fee,
                total_amount=rent_fee.total_amount + float(late_fee)
            ))

    # Update booking status to returned
    bookingmodel=update(db, db_obj, BookingUpdateSchema(status=2, drop_location=item_in.drop_location, drop_time=current_time))

    # Notify observers about car return
    booking_subject.notify_observers(bookingmodel, "returned")
    return bookingmodel
