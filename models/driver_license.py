from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Numeric, event,Date,Time
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class DriverLicenseModel(Base):
    __tablename__ = 'driver_license'

    driver_license_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), nullable=True)
    license_pic = Column(String(), nullable=True)
    expire_date = Column(Date(), nullable=True)
    is_verified = Column(Integer(), nullable=True,default=0)
    create_time = Column(DateTime(), nullable=True)
    modify_time = Column(DateTime(), nullable=True)
    is_deleted = Column(Integer(), nullable=True,default=0)
    drive_number = Column(String(), nullable=True)
@event.listens_for(DriverLicenseModel, "before_update", propagate=True)
def receive_before_update(mapper, connection, target):
    target.modify_time = datetime.now()
@event.listens_for(DriverLicenseModel, "before_insert", propagate=True) 
def receive_before_insert(mapper, connection, target):
    target.create_time = datetime.now()
    target.modify_time = datetime.now()
