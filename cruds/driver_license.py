from sqlalchemy.orm import Session
from models.driver_license import DriverLicenseModel
from schemas.driver_license import DriverLicenseSchema,DriverLicenseCreateSchema,DriverLicenseUpdateSchema

# CRUD Functions

def get_all(session: Session):
    return session.query(DriverLicenseModel).all()

def get_by_user_id(session: Session, user_id):
    return session.query(DriverLicenseModel).filter_by(user_id=user_id).filter_by(is_deleted=0).first()

def get(session: Session, driver_license_id):
    return session.query(DriverLicenseModel).filter_by(driver_license_id=driver_license_id).first()

def create(session: Session, obj_in: DriverLicenseCreateSchema):
    obj = DriverLicenseModel(**obj_in.dict())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update(session: Session, db_obj: DriverLicenseModel, obj_in: DriverLicenseUpdateSchema):
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def delete(session: Session, db_obj: DriverLicenseModel):
    session.delete(db_obj)
    session.commit()
    return True
