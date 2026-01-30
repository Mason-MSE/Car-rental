from pydantic import BaseModel,Field, constr
from datetime import datetime, date, time
from typing import Optional

class RoleSchema(BaseModel):
    id: Optional[int] = None
    role_name: Optional[str] = Field(None, max_length=50)
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

class RoleCreateSchema(BaseModel):
    role_name: Optional[str] = Field(None, max_length=50)

    class Config:
        from_attributes = True

class RoleUpdateSchema(BaseModel):
    is_deleted: Optional[int] = None

    class Config:
        from_attributes = True
