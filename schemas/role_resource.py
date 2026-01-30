from pydantic import BaseModel,Field, constr
from datetime import datetime, date, time
from typing import Optional

class RoleResourceSchema(BaseModel):
    id: Optional[int] = None
    role_id: Optional[int] = None
    resource_id: Optional[int] = None
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

class RoleResourceCreateSchema(BaseModel):
    id: int
    role_id: Optional[int] = None
    resource_id: Optional[int] = None
    create_time: Optional[datetime] = None
    modify_time: Optional[datetime] = None
    is_deleted: Optional[int] = None

    class Config:
        from_attributes = True

class RoleResourceUpdateSchema(BaseModel):
    is_deleted: Optional[int] = None

    class Config:
        from_attributes = True
