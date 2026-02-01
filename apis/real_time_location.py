from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from cruds.real_time_location import (
    get_all,
    get,
    get_by_car_id,
    get_latest_by_car_id,
    create,
    update,
    delete,
)
from schemas.real_time_location import (
    RealTimeLocationSchema,
    RealTimeLocationCreateSchema,
    RealTimeLocationUpdateSchema,
)

router = APIRouter(prefix="/real_time_location", tags=["realtimelocation"])

# -------------------------------
# Get all location records
# -------------------------------
@router.get("/", response_model=List[RealTimeLocationSchema])
def read_locations(db: Session = Depends(get_db)):
    return get_all(db)

# -------------------------------
# Get a single location record by ID
# -------------------------------
@router.get("/{location_id}", response_model=RealTimeLocationSchema)
def read_location(location_id: int, db: Session = Depends(get_db)):
    obj = get(db, location_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Location not found")
    return obj

# -------------------------------
# Get all locations for a car
# -------------------------------
@router.get("/car/{car_id}", response_model=List[RealTimeLocationSchema])
def read_locations_by_car(car_id: int, db: Session = Depends(get_db)):
    return get_by_car_id(db, car_id)

# -------------------------------
# Get latest location for a car
# -------------------------------
@router.get("/car/{car_id}/latest", response_model=RealTimeLocationSchema)
def read_latest_location_by_car(car_id: int, db: Session = Depends(get_db)):
    obj = get_latest_by_car_id(db, car_id)
    if not obj:
        raise HTTPException(status_code=404, detail="No location data for this car")
    return obj

# -------------------------------
# Create a new location record
# -------------------------------
@router.post("/", response_model=RealTimeLocationSchema)
def create_location(obj_in: RealTimeLocationCreateSchema, db: Session = Depends(get_db)):
    return create(db, obj_in)

# -------------------------------
# Update a location record
# -------------------------------
@router.put("/{location_id}", response_model=RealTimeLocationSchema)
def update_location(location_id: int, obj_in: RealTimeLocationUpdateSchema, db: Session = Depends(get_db)):
    db_obj = get(db, location_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Location not found")
    return update(db, db_obj, obj_in)

# -------------------------------
# Delete a location record
# -------------------------------
@router.delete("/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_obj = get(db, location_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Location not found")
    delete(db, db_obj)
    return {"detail": "Location deleted successfully"}
