from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.booking import BookingUpdateSchema
from schemas.payment import PaymentSchema,PaymentCreateSchema,PaymentUpdateSchema
from cruds.payment import get, get_all, create, get_by_booking_id, update, delete
import cruds.booking as booking_crud




def create_item(item_in, db):
    payment_model = get_by_booking_id(db,item_in.booking_id)
    if payment_model:
        raise HTTPException(status_code=400, detail='Payment already payed')
    payment=create(db, item_in)
    bookingid=item_in.booking_id
    bookingmodel=booking_crud.get(db,bookingid) 
    if not bookingmodel:
        raise HTTPException(status_code=400, detail='Associated booking does not exist')
    booking_crud.update(db,bookingmodel,BookingUpdateSchema(status=3))
    return payment