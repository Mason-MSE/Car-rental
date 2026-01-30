from sqlalchemy.orm import Session
from models.insurance import InsuranceModel
from schemas.insurance import (
    InsuranceSchema,
    InsuranceCreateSchema,
    InsuranceUpdateSchema
)

def get_all(session: Session):
    return (
        session.query(InsuranceModel)
        .filter(InsuranceModel.is_deleted == 0)
        .all()
    )

def get(session: Session, id: int):
    return (
        session.query(InsuranceModel)
        .filter(
            InsuranceModel.id == id,
            InsuranceModel.is_deleted == 0
        )
        .first()
    )


def create(
    session: Session,
    obj_in: InsuranceCreateSchema,
    user_id: int
):
    obj = InsuranceModel(
        **obj_in.dict(),
        user_id=user_id
    )
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def update(
    session: Session,
    db_obj: InsuranceModel,
    obj_in: InsuranceUpdateSchema
):
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)

    session.commit()
    session.refresh(db_obj)
    return db_obj


def delete(session: Session, db_obj: InsuranceModel):
    db_obj.is_deleted = 1
    session.commit()
    return True


def get_by_booking(session: Session, booking_id: int):
    return (
        session.query(InsuranceModel)
        .filter(
            InsuranceModel.booking_id == booking_id,
            InsuranceModel.is_deleted == 0
        )
        .all()
    )
def get_by_user(session: Session, user_id: int):
    return (
        session.query(InsuranceModel)
        .filter(
            InsuranceModel.user_id == user_id,
            InsuranceModel.is_deleted == 0
        )
        .all()
    )