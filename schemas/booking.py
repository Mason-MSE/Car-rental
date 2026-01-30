from pydantic import BaseModel,Field, constr
from datetime import datetime, date, time
from typing import Optional

class BookingSchema(BaseModel):
    booking_id: Optional[int] = None
    user_id: Optional[int] = None
    car_id: Optional[int] = None
    insurance_price_id: Optional[int]=None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    pickup_location: Optional[int] = None
    pickup_time: Optional[datetime] = None
    drop_location: Optional[int] = None
    drop_time: Optional[datetime] = None
    status: Optional[int] = None
    notes: Optional[str] = None
    create_time: Optional[datetime] = None
    modify_time: Optional[datetime] = None
    is_deleted: Optional[int] = None

    class Config:
        from_attributes = True
        extra = "ignore"
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S') if v else None,
            date: lambda v: v.strftime('%Y-%m-%d') if v else None,
            time: lambda v: v.strftime('%H:%M:%S') if v else None,
        }

class BookingCreateSchema(BaseModel):
    user_id: Optional[int] = None
    car_id: Optional[int] = None
    insurance_price_id: Optional[int]=None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    pickup_location: Optional[int] = None
    drop_location: Optional[int] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
        extra = "ignore"

class BookingUpdateSchema(BaseModel):
    user_id: Optional[int] = None
    car_id: Optional[int] = None
    insurance_price_id: Optional[int]=None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    pickup_location: Optional[int] = None
    drop_location: Optional[int] = None
    drop_time: Optional[datetime] = None
    status: Optional[int] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
class BookingReturnCarSchema(BaseModel):
    booking_id: Optional[int] = None
    end_date: Optional[datetime] = None
    drop_location: Optional[int] = None

    class Config:
        from_attributes = True
        
class BookingApprovalSchema(BaseModel):
    status: Optional[int] = None
    notes: Optional[str] = None
    class Config:
        from_attributes = True