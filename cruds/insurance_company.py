# cruds/insurance_company.py
from sqlalchemy.orm import Session
from models.insurance import InsuranceCompanyModel
from schemas.insurance import (
    InsuranceCompanyCreateSchema,
    InsuranceCompanyUpdateSchema
)

def get_all(session: Session):
    return session.query(InsuranceCompanyModel).filter(InsuranceCompanyModel.is_deleted==0).all()

def get(session: Session, id: int):
    return session.query(InsuranceCompanyModel).filter(InsuranceCompanyModel.id==id, InsuranceCompanyModel.is_deleted==0).first()

def create(session: Session, obj_in: InsuranceCompanyCreateSchema):
    obj = InsuranceCompanyModel(**obj_in.dict())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update(session: Session, db_obj: InsuranceCompanyModel, obj_in: InsuranceCompanyUpdateSchema):
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def delete(session: Session, db_obj: InsuranceCompanyModel):
    db_obj.is_deleted = 1
    session.commit()
    return True
