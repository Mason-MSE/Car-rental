from pydantic import BaseModel,Field, constr
from datetime import datetime, date, time
from typing import Optional

class CarSchema(BaseModel):
    car_id: Optional[int] = None
    make: Optional[str] = Field(None, max_length=50)
    model: Optional[str] = Field(None, max_length=50)
    year: Optional[int] = None
    mileage: Optional[int] = None
    is_available: Optional[int] = None
    min_days: Optional[int] = None
    max_days: Optional[int] = None
    license_plate: Optional[str] = Field(None, max_length=20)
    color: Optional[str] = Field(None, max_length=20)
    daily_rate: Optional[float] = None
    category_id: Optional[int] = None
    location_id: Optional[int] = None
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

class CarCreateSchema(BaseModel):
    car_id: int
    make: Optional[str] = Field(None, max_length=50)
    model: Optional[str] = Field(None, max_length=50)
    year: Optional[int] = None
    mileage: Optional[int] = None
    is_available: Optional[int] = None
    min_days: Optional[int] = None
    max_days: Optional[int] = None
    license_plate: Optional[str] = Field(None, max_length=20)
    color: Optional[str] = Field(None, max_length=20)
    daily_rate: Optional[float] = None
    category_id: Optional[int] = None
    location_id: Optional[int] = None
    create_time: Optional[datetime] = None
    modify_time: Optional[datetime] = None
    is_deleted: Optional[int] = None

    class Config:
        from_attributes = True

class CarUpdateSchema(BaseModel):
    make: Optional[str] = Field(None, max_length=50)
    model: Optional[str] = Field(None, max_length=50)
    year: Optional[int] = None
    mileage: Optional[int] = None
    is_available: Optional[int] = None
    min_days: Optional[int] = None
    max_days: Optional[int] = None
    license_plate: Optional[str] = Field(None, max_length=20)
    color: Optional[str] = Field(None, max_length=20)
    daily_rate: Optional[float] = None
    category_id: Optional[int] = None
    location_id: Optional[int] = None
    is_deleted: Optional[int] = None

    class Config:
        from_attributes = True
