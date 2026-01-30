from sqlalchemy.orm import Session
from models.payment import PaymentModel
from schemas.payment import PaymentSchema,PaymentCreateSchema,PaymentUpdateSchema

# CRUD Functions

def get_all(session: Session):
    return session.query(PaymentModel).all()

def get(session: Session, payment_id):
    return session.query(PaymentModel).filter_by(payment_id=payment_id).first()

def get_by_booking_id(session: Session, booking_id):
    return session.query(PaymentModel).filter_by(booking_id=booking_id).first()


def create(session: Session, obj_in: PaymentCreateSchema):
    obj = PaymentModel(**obj_in.dict())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update(session: Session, db_obj: PaymentModel, obj_in: PaymentUpdateSchema):
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def delete(session: Session, db_obj: PaymentModel):
    session.delete(db_obj)
    session.commit()
    return True
