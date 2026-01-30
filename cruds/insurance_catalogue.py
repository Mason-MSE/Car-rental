from sqlalchemy.orm import Session
from models.insurance import InsuranceCatalogueModel
from schemas.insurance import (
    InsuranceCatalogueCreateSchema,
    InsuranceCatalogueUpdateSchema
)

def get_all(session: Session):
    return session.query(InsuranceCatalogueModel).filter(InsuranceCatalogueModel.is_deleted==0).all()

def get(session: Session, id: int):
    return session.query(InsuranceCatalogueModel).filter(
        InsuranceCatalogueModel.id==id, InsuranceCatalogueModel.is_deleted==0
    ).first()

def create(session: Session, obj_in: InsuranceCatalogueCreateSchema):
    obj = InsuranceCatalogueModel(**obj_in.dict())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update(session: Session, db_obj: InsuranceCatalogueModel, obj_in: InsuranceCatalogueUpdateSchema):
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def delete(session: Session, db_obj: InsuranceCatalogueModel):
    db_obj.is_deleted = 1
    session.commit()
    return True
