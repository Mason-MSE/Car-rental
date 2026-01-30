from sqlalchemy.orm import Session
from models.location import LocationModel
from schemas.location import LocationSchema,LocationCreateSchema,LocationUpdateSchema

# CRUD Functions

def get_all(session: Session):
    return session.query(LocationModel).all()

def get(session: Session, id):
    return session.query(LocationModel).filter_by(id=id).first()

def create(session: Session, obj_in: LocationCreateSchema):
    obj = LocationModel(**obj_in.dict())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update(session: Session, db_obj: LocationModel, obj_in: LocationUpdateSchema):
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def delete(session: Session, db_obj: LocationModel):
    session.delete(db_obj)
    session.commit()
    return True
