from sqlalchemy.orm import Session
from models.car import CarModel
from schemas.car import CarSchema,CarCreateSchema,CarUpdateSchema

# CRUD Functions

def get_all(session: Session):
    return session.query(CarModel).filter_by(is_deleted=0).filter_by(is_available=1).all()

def get(session: Session, car_id):
    return session.query(CarModel).filter_by(car_id=car_id).first()

def create(session: Session, obj_in: CarCreateSchema):
    obj = CarModel(**obj_in.dict())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update(session: Session, db_obj: CarModel, obj_in: CarUpdateSchema):
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def delete(session: Session, db_obj: CarModel):
    session.delete(db_obj)
    session.commit()
    return True
