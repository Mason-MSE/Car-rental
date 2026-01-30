from sqlalchemy.orm import Session
from models.user_role import UserRoleModel
from schemas.user_role import UserRoleSchema,UserRoleCreateSchema,UserRoleUpdateSchema

# CRUD Functions

def get_all(session: Session):
    return session.query(UserRoleModel).all()

def get(session: Session, user_id, role_id):
    return session.query(UserRoleModel).filter_by(user_id=user_id, role_id=role_id).first()

def create(session: Session, obj_in: UserRoleCreateSchema):
    obj = UserRoleModel(**obj_in.dict())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update(session: Session, db_obj: UserRoleModel, obj_in: UserRoleUpdateSchema):
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def delete(session: Session, db_obj: UserRoleModel):
    session.delete(db_obj)
    session.commit()
    return True
