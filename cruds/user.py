from sqlalchemy.orm import Session
from models.user import UserModel
from schemas.user import UserSchema,UserCreateSchema,UserUpdateSchema

# CRUD Functions

def get_all(session: Session):
    return session.query(UserModel).all()

def get(session: Session, id):
    return session.query(UserModel).filter_by(id=id).first()

def create(session: Session, obj_in: UserCreateSchema):
    obj = UserModel(**obj_in.dict())
    obj.set_password(obj.password)  # Hash the password before storing
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update(session: Session, db_obj: UserModel, obj_in: UserUpdateSchema):
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def delete(session: Session, db_obj: UserModel):
    session.delete(db_obj)
    session.commit()
    return True

def soft_delete(session: Session, db_obj: UserModel):
    db_obj.is_deleted = 1
    update(session, db_obj, UserUpdateSchema(is_deleted=1))
    session.commit()
    return True
