from pydantic import BaseModel,Field, constr
from datetime import datetime, date, time
from typing import Optional

class CarCategorySchema(BaseModel):
    id: Optional[int] = None
    category_name: Optional[str] = Field(None, max_length=50)
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

class CarCategoryCreateSchema(BaseModel):
    id: int
    category_name: Optional[str] = Field(None, max_length=50)
    create_time: Optional[datetime] = None
    modify_time: Optional[datetime] = None
    is_deleted: Optional[int] = None

    class Config:
        from_attributes = True

class CarCategoryUpdateSchema(BaseModel):
    is_deleted: Optional[int] = None

    class Config:
        from_attributes = True
