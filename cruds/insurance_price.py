from sqlalchemy.orm import Session
from models.insurance import InsurancePriceModel
from schemas.insurance import (
    InsurancePriceCreateSchema,
    InsurancePriceUpdateSchema
)

def get_all(session: Session):
    return session.query(InsurancePriceModel).filter(InsurancePriceModel.is_deleted==0).all()

def get(session: Session, id: int):
    return session.query(InsurancePriceModel).filter(
        InsurancePriceModel.id==id, InsurancePriceModel.is_deleted==0
    ).first()

def create(session: Session, obj_in: InsurancePriceCreateSchema):
    obj = InsurancePriceModel(**obj_in.dict())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update(session: Session, db_obj: InsurancePriceModel, obj_in: InsurancePriceUpdateSchema):
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def delete(session: Session, db_obj: InsurancePriceModel):
    db_obj.is_deleted = 1
    session.commit()
    return True
