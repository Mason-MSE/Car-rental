from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Numeric, event,Date,Time
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class BookingModel(Base):
    __tablename__ = 'booking'

    booking_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), nullable=True)
    car_id = Column(Integer(), nullable=True)
    start_date = Column(DateTime(), nullable=True)
    end_date = Column(DateTime(), nullable=True)
    pickup_location = Column(Integer(), nullable=True)
    pickup_time = Column(DateTime(), nullable=True)
    drop_location = Column(Integer(), nullable=True)
    drop_time = Column(DateTime(), nullable=True)
    status = Column(Integer(), nullable=True,default=0)
    notes = Column(String(), nullable=True)
    create_time = Column(DateTime(), nullable=True)
    modify_time = Column(DateTime(), nullable=True)
    is_deleted = Column(Integer(), nullable=True,default=0)

@event.listens_for(BookingModel, "before_update", propagate=True)
def receive_before_update(mapper, connection, target):  
    target.modify_time = datetime.now() 

@event.listens_for(BookingModel, "before_insert", propagate=True)
def receive_before_insert(mapper, connection, target):  
    target.create_time = datetime.now() 
    target.modify_time = datetime.now()