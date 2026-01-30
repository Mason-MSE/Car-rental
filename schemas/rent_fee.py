from pydantic import BaseModel,Field, constr
from datetime import datetime, date, time
from typing import Optional

class RentFeeSchema(BaseModel):
    rent_fee_id: Optional[int] = None
    booking_id: Optional[int] = None
    base_amount: Optional[float] = None
    insurance_amount: Optional[float] = None
    late_fee: Optional[float] = None
    discount_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
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

class RentFeeCreateSchema(BaseModel):
    booking_id: Optional[int] = None
    base_amount: Optional[float] = None
    insurance_amount: Optional[float] = None
    late_fee: Optional[float] = None
    discount_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None

    class Config:
        from_attributes = True

class RentFeeUpdateSchema(BaseModel):
    base_amount: Optional[float] = None
    insurance_amount: Optional[float] = None
    late_fee: Optional[float] = None
    discount_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None

    class Config:
        from_attributes = True
