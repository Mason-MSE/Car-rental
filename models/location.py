from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Numeric, event,Date,Time
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class LocationModel(Base):
    __tablename__ = 'location'

    id = Column(Integer(), primary_key=True)
    location_name = Column(String(), nullable=True)
    street = Column(String(), nullable=True)
    city = Column(String(), nullable=True)
    state = Column(String(), nullable=True)
    zipcode = Column(String(), nullable=True)
    create_time = Column(DateTime(), nullable=True)
    modify_time = Column(DateTime(), nullable=True)
    is_deleted = Column(Integer(), nullable=True,default=0)
@event.listens_for(LocationModel, "before_update", propagate=True)
def receive_before_update(mapper, connection, target):  
    target.modify_time = datetime.now()
@event.listens_for(LocationModel, "before_insert", propagate=True)
def receive_before_insert(mapper, connection, target):  
    target.create_time = datetime.now() 
    target.modify_time = datetime.now()
