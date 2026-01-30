from sqlalchemy.orm import Session
from models.resource import ResourceModel
from schemas.resource import ResourceSchema,ResourceCreateSchema,ResourceUpdateSchema

# CRUD Functions

def get_all(session: Session):
    return session.query(ResourceModel).all()

def get(session: Session, id):
    return session.query(ResourceModel).filter_by(id=id).first()

def create(session: Session, obj_in: ResourceCreateSchema):
    obj = ResourceModel(**obj_in.dict())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update(session: Session, db_obj: ResourceModel, obj_in: ResourceUpdateSchema):
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def delete(session: Session, db_obj: ResourceModel):
    session.delete(db_obj)
    session.commit()
    return True
