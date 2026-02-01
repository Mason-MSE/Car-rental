from sqlalchemy.orm import Session
from models.real_time_location import RealTimeLocationModel
from schemas.real_time_location import (
    RealTimeLocationSchema,
    RealTimeLocationCreateSchema,
    RealTimeLocationUpdateSchema,
)

# -----------------------------
# CRUD Functions for RealTimeLocation
# -----------------------------

def get_all(session: Session):
    """Return all location records"""
    return session.query(RealTimeLocationModel).all()

def get(session: Session, id: int):
    """Get a single location record by its ID"""
    return session.query(RealTimeLocationModel).filter_by(id=id).first()

def get_by_car_id(session: Session, car_id: int):
    """Get all location records for a specific car"""
    return session.query(RealTimeLocationModel).filter_by(car_id=car_id).all()

def get_latest_by_car_id(session: Session, car_id: int):
    """Get the latest location record for a specific car"""
    return (
        session.query(RealTimeLocationModel)
        .filter_by(car_id=car_id)
        .order_by(RealTimeLocationModel.timestamp.desc())
        .first()
    )

def create(session: Session, obj_in: RealTimeLocationCreateSchema):
    """Create a new location record"""
    obj_data = obj_in.dict()
    if not obj_data.get("timestamp"):
        obj_data["timestamp"] = datetime.now()  # auto-fill timestamp
    obj = RealTimeLocationModel(**obj_data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update(session: Session, db_obj: RealTimeLocationModel, obj_in: RealTimeLocationUpdateSchema):
    """Update an existing location record"""
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def delete(session: Session, db_obj: RealTimeLocationModel):
    """Delete a location record"""
    session.delete(db_obj)
    session.commit()
    return True
