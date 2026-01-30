from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.rent_fee import RentFeeSchema,RentFeeCreateSchema,RentFeeUpdateSchema
from cruds.rent_fee import get, get_all, create, update, delete

router = APIRouter(prefix='/rent_fee', tags=['rent_fee'])

@router.get('/', response_model=List[RentFeeSchema])
def read_all(db: Session = Depends(get_db)):
    return get_all(db)

@router.get('/{rent_fee_id}', response_model=RentFeeSchema)
def read_item(rent_fee_id, db: Session = Depends(get_db)):
    db_obj = get(db, rent_fee_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return db_obj

@router.post('/', response_model=RentFeeSchema)
def create_item(item_in: RentFeeCreateSchema, db: Session = Depends(get_db)):
    return create(db, item_in)

@router.put('/{rent_fee_id}', response_model=RentFeeSchema)
def update_item(rent_fee_id, item_in: RentFeeUpdateSchema, db: Session = Depends(get_db)):
    db_obj = get(db, rent_fee_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return update(db, db_obj, item_in)

@router.delete('/{rent_fee_id}')
def delete_item(rent_fee_id, db: Session = Depends(get_db)):
    db_obj = get(db, rent_fee_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    delete(db, db_obj)
    return {'ok': True}
