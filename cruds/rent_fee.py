from sqlalchemy.orm import Session
from models.rent_fee import RentFeeModel
from schemas.rent_fee import RentFeeSchema,RentFeeCreateSchema,RentFeeUpdateSchema

# CRUD Functions

def get_all(session: Session):
    return session.query(RentFeeModel).all()

def get(session: Session, rent_fee_id):
    return session.query(RentFeeModel).filter_by(rent_fee_id=rent_fee_id).first()

def get_by_booking_id(session: Session, booking_id):
    return session.query(RentFeeModel).filter_by(booking_id=booking_id).filter_by(is_deleted=0).first()

def create(session: Session, obj_in: RentFeeCreateSchema):
    obj = RentFeeModel(**obj_in.dict())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update(session: Session, db_obj: RentFeeModel, obj_in: RentFeeUpdateSchema):
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def delete(session: Session, db_obj: RentFeeModel):
    session.delete(db_obj)
    session.commit()
    return True
