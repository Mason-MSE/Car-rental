from sqlalchemy.orm import Session
from models.role_resource import RoleResourceModel
from schemas.role_resource import RoleResourceSchema,RoleResourceCreateSchema,RoleResourceUpdateSchema

# CRUD Functions

def get_all(session: Session):
    return session.query(RoleResourceModel).all()

def get(session: Session, id):
    return session.query(RoleResourceModel).filter_by(id=id).first()

def create(session: Session, obj_in: RoleResourceCreateSchema):
    obj = RoleResourceModel(**obj_in.dict())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update(session: Session, db_obj: RoleResourceModel, obj_in: RoleResourceUpdateSchema):
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def delete(session: Session, db_obj: RoleResourceModel):
    session.delete(db_obj)
    session.commit()
    return True
