from sqlalchemy.orm import Session
from models.booking import BookingModel
from schemas.booking import BookingSchema,BookingCreateSchema,BookingUpdateSchema


# CRUD Functions

def get_all(session: Session):
    return session.query(BookingModel).all()

def get(session: Session, booking_id):
    return session.query(BookingModel).filter_by(booking_id=booking_id).first()

def create(session: Session, obj_in: BookingCreateSchema):
    data=obj_in.dict(exclude={"insurance_price_id"})
    obj = BookingModel(**data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update(session: Session, db_obj: BookingModel, obj_in: BookingUpdateSchema):
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def delete(session: Session, db_obj: BookingModel):
    session.delete(db_obj)
    session.commit()
    return True
