from pydantic import BaseModel,Field, constr
from datetime import datetime, date, time
from typing import Optional

class UserProfileSchema(BaseModel):
    profile_id: Optional[int] = None
    user_id: Optional[int] = None
    street: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=50)
    state_name: Optional[str] = Field(None, max_length=50)
    zipcode: Optional[str] = Field(None, max_length=20)
    membership_type: Optional[int] = None
    driver_license_id: Optional[int] = None
    avatar_url: Optional[str] = Field(None, max_length=255)
    date_of_birth: Optional[date] = None
    nationality: Optional[str] = Field(None, max_length=50)
    emergency_contact_name: Optional[str] = Field(None, max_length=100)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)
    preferred_language: Optional[str] = Field(None, max_length=20)
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

class UserProfileCreateSchema(BaseModel):
    user_id: Optional[int] = None
    street: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=50)
    state_name: Optional[str] = Field(None, max_length=50)
    zipcode: Optional[str] = Field(None, max_length=20)
    membership_type: Optional[int] = None
    driver_license_id: Optional[int] = None
    avatar_url: Optional[str] = Field(None, max_length=255)
    date_of_birth: Optional[date] = None
    nationality: Optional[str] = Field(None, max_length=50)
    emergency_contact_name: Optional[str] = Field(None, max_length=100)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)
    preferred_language: Optional[str] = Field(None, max_length=20)

    class Config:
        from_attributes = True

class UserProfileUpdateSchema(BaseModel):
    is_deleted: Optional[int] = None

    class Config:
        from_attributes = True
