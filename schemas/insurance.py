from pydantic import BaseModel, Field, constr
from datetime import datetime, date, time
from typing import Optional

class InsuranceSchema(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    booking_id: Optional[int] = None
    insurance_price_id: Optional[int]=None

    insurance_type: Optional[int] = None
    policy_number: Optional[str] = None
    provider: Optional[str] = None

    coverage_amount: Optional[float] = None
    premium: Optional[float] = None

    start_date: Optional[date] = None
    end_date: Optional[date] = None

    status: Optional[int] = None
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
class InsuranceCreateSchema(BaseModel):
    booking_id: int
    insurance_type: int
    policy_number: Optional[str] = Field(None, max_length=50)
    provider: Optional[str] = Field(None, max_length=50)
    insurance_price_id: int
    coverage_amount: float = Field(..., gt=0)
    premium: float = Field(..., gt=0)
    start_date: date
    end_date: date

    class Config:
        from_attributes = True


class InsuranceUpdateSchema(BaseModel):
    insurance_type: Optional[int] = None
    provider: Optional[str] = None
    insurance_price_id:Optional[int]=None
    coverage_amount: Optional[float] = Field(None, gt=0)
    premium: Optional[float] = Field(None, gt=0)

    start_date: Optional[date] = None
    end_date: Optional[date] = None

    status: Optional[int] = None

    class Config:
        from_attributes = True

class InsuranceDeleteSchema(BaseModel):
    is_deleted: Optional[int] = 1

    class Config:
        from_attributes = True


from enum import IntEnum

class InsuranceType(IntEnum):
    DRIVER = 1
    RENTAL = 2
    VEHICLE = 3

class InsuranceStatus(IntEnum):
    ACTIVE = 1
    EXPIRED = 2
    CANCELLED = 3


class InsuranceCompanySchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    status: Optional[int] = None
    create_time: Optional[datetime] = None
    modify_time: Optional[datetime] = None
    is_deleted: Optional[int] = None

    class Config:
        from_attributes = True

class InsuranceCompanyCreateSchema(BaseModel):
    name: Optional[str]=None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None

    class Config:
        from_attributes = True

class InsuranceCompanyUpdateSchema(BaseModel):
    name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    status: Optional[int] = None

    class Config:
        from_attributes = True


class InsuranceCatalogueSchema(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    company_id: Optional[int] = None
    insurance_type: Optional[int] = None
    status: Optional[int] = None
    create_time: Optional[datetime] = None
    modify_time: Optional[datetime] = None
    is_deleted: Optional[int] = None

    class Config:
        from_attributes = True

class InsuranceCatalogueCreateSchema(BaseModel):
    code: Optional[str]=Field(None, max_length=100)
    name: Optional[str]=Field(None,max_length=100)
    description: Optional[str] = None
    company_id: int
    insurance_type: int

    class Config:
        from_attributes = True

class InsuranceCatalogueUpdateSchema(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    company_id: Optional[int] = None
    insurance_type: Optional[int] = None
    status: Optional[int] = None

    class Config:
        from_attributes = True

class InsurancePriceSchema(BaseModel):
    id: Optional[int] = None
    catalogue_id: Optional[int] = None
    coverage_amount: Optional[float] = None
    premium: Optional[float] = None
    duration_days: Optional[int] = None
    status: Optional[int] = None
    create_time: Optional[datetime] = None
    modify_time: Optional[datetime] = None
    is_deleted: Optional[int] = None

    class Config:
        from_attributes = True

class InsurancePriceCreateSchema(BaseModel):
    catalogue_id: int
    coverage_amount: float
    premium: float
    duration_days: int

    class Config:
        from_attributes = True

class InsurancePriceUpdateSchema(BaseModel):
    catalogue_id: Optional[int] = None
    coverage_amount: Optional[float] = None
    premium: Optional[float] = None
    duration_days: Optional[int] = None
    status: Optional[int] = None

    class Config:
        from_attributes = True