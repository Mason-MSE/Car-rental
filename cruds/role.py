from sqlalchemy.orm import Session
from models.role import RoleModel
from schemas.role import RoleSchema,RoleCreateSchema,RoleUpdateSchema

# CRUD Functions

def get_all(session: Session):
    return session.query(RoleModel).all()

def get(session: Session, id):
    return session.query(RoleModel).filter_by(id=id).first()

def create(session: Session, obj_in: RoleCreateSchema):
    obj = RoleModel(**obj_in.dict())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update(session: Session, db_obj: RoleModel, obj_in: RoleUpdateSchema):
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def delete(session: Session, db_obj: RoleModel):
    session.delete(db_obj)
    session.commit()
    return True
