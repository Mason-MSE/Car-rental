from sqlalchemy.orm import Session
from models.car_category import CarCategoryModel
from schemas.car_category import CarCategorySchema,CarCategoryCreateSchema,CarCategoryUpdateSchema

# CRUD Functions

def get_all(session: Session):
    return session.query(CarCategoryModel).all()

def get(session: Session, id):
    return session.query(CarCategoryModel).filter_by(id=id).first()

def create(session: Session, obj_in: CarCategoryCreateSchema):
    obj = CarCategoryModel(**obj_in.dict())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update(session: Session, db_obj: CarCategoryModel, obj_in: CarCategoryUpdateSchema):
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def delete(session: Session, db_obj: CarCategoryModel):
    session.delete(db_obj)
    session.commit()
    return True
