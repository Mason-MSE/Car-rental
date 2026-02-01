from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class RealTimeLocationSchema(BaseModel):
    """Schema for returning real-time location data"""
    id: Optional[int] = None
    car_id: int
    latitude: float
    longitude: float
    speed: Optional[float] = 0.0       # km/h
    heading: Optional[float] = 0.0     # 0-360 degrees
    status: Optional[int] = 1          # 0=idle,1=active,2=offline
    timestamp: Optional[datetime] = None
    create_time: Optional[datetime] = None
    modify_time: Optional[datetime] = None
    is_deleted: Optional[int] = 0

    class Config:
        from_attributes = True
        extra = "ignore"
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S') if v else None,
        }

class RealTimeLocationCreateSchema(BaseModel):
    """Schema for creating a new location record"""
    car_id: int
    latitude: float
    longitude: float
    speed: Optional[float] = 0.0
    heading: Optional[float] = 0.0
    status: Optional[int] = 1
    timestamp: Optional[datetime] = None  # default to current time if not provided

    class Config:
        from_attributes = True
        extra = "ignore"

class RealTimeLocationUpdateSchema(BaseModel):
    """Schema for updating an existing location record"""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    speed: Optional[float] = None
    heading: Optional[float] = None
    status: Optional[int] = None
    timestamp: Optional[datetime] = None  # update time if provided

    class Config:
        from_attributes = True
        extra = "ignore"
