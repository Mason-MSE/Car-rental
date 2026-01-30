from pydantic import BaseModel,Field, constr
from datetime import datetime, date, time
from typing import Optional

class PaymentSchema(BaseModel):
    payment_id: Optional[int] = None
    booking_id: Optional[int] = None
    rent_fee_id: Optional[int] = None
    payment_amount: Optional[float] = None
    payment_date: Optional[datetime] = None
    payment_method: Optional[str] = None
    payment_status: Optional[int] = None
    reference_number: Optional[str] = Field(None, max_length=50)
    payer_name: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None
    create_time: Optional[datetime] = None
    modify_time: Optional[datetime] = None
    is_deleted: Optional[int] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S') if v else None,
            date: lambda v: v.strftime('%Y-%m-%d') if v else None,
            time: lambda v: v.strftime('%H:%M:%S') if v else None,
        }

class PaymentCreateSchema(BaseModel):
    booking_id: Optional[int] = None
    rent_fee_id: Optional[int] = None
    payment_amount: Optional[float] = None
    payment_date: Optional[datetime] = None
    payment_method: Optional[str] = None
    payment_status: Optional[int] = None
    reference_number: Optional[str] = Field(None, max_length=50)
    payer_name: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True

class PaymentUpdateSchema(BaseModel):
    is_deleted: Optional[int] = None

    class Config:
        from_attributes = True
