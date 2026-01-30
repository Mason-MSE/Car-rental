from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Numeric, event,Date,Time
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class CarModel(Base):
    __tablename__ = 'car'

    car_id = Column(Integer(), primary_key=True)
    make = Column(String(), nullable=True)
    model = Column(String(), nullable=True)
    year = Column(Integer(), nullable=True)
    mileage = Column(Integer(), nullable=True)
    is_available = Column(Integer(), nullable=True)
    min_days = Column(Integer(), nullable=True)
    max_days = Column(Integer(), nullable=True)
    license_plate = Column(String(), nullable=True)
    color = Column(String(), nullable=True)
    daily_rate = Column(Float(), nullable=True)
    category_id = Column(Integer(), nullable=True)
    location_id = Column(Integer(), nullable=True)
    create_time = Column(DateTime(), nullable=True)
    modify_time = Column(DateTime(), nullable=True)
    is_deleted = Column(Integer(), nullable=True,default=0)
@event.listens_for(CarModel, "before_update", propagate=True)
def receive_before_update(mapper, connection, target):      
    target.modify_time = datetime.now()                 
@event.listens_for(CarModel, "before_insert", propagate=True)
def receive_before_insert(mapper, connection, target):  
    target.create_time = datetime.now()                 
    target.modify_time = datetime.now()
