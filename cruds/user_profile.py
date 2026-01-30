from sqlalchemy.orm import Session
from models.user_profile import UserProfileModel
from schemas.user_profile import UserProfileSchema,UserProfileCreateSchema,UserProfileUpdateSchema

# CRUD Functions

def get_all(session: Session):
    return session.query(UserProfileModel).all()

def get_by_user_id(session: Session, user_id):
    return session.query(UserProfileModel).filter_by(user_id=user_id).filter_by(is_deleted=0).first()

def get(session: Session, profile_id):
    return session.query(UserProfileModel).filter_by(profile_id=profile_id).first()

def create(session: Session, obj_in: UserProfileCreateSchema):
    obj = UserProfileModel(**obj_in.dict())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update(session: Session, db_obj: UserProfileModel, obj_in: UserProfileUpdateSchema):
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def delete(session: Session, db_obj: UserProfileModel):
    session.delete(db_obj)
    session.commit()
    return True
