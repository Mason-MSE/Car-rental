from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Numeric, event,Date,Time
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class UserProfileModel(Base):
    __tablename__ = 'user_profile'

    profile_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), nullable=True)
    street = Column(String(), nullable=True)
    city = Column(String(), nullable=True)
    state_name = Column(String(), nullable=True)
    zipcode = Column(String(), nullable=True)
    membership_type = Column(Integer(), nullable=True)
    driver_license_id = Column(Integer(), nullable=True)
    avatar_url = Column(String(), nullable=True)
    date_of_birth = Column(Date(), nullable=True)
    nationality = Column(String(), nullable=True)
    emergency_contact_name = Column(String(), nullable=True)
    emergency_contact_phone = Column(String(), nullable=True)
    preferred_language = Column(String(), nullable=True)
    create_time = Column(DateTime(), nullable=True)
    modify_time = Column(DateTime(), nullable=True)
    is_deleted = Column(Integer(), nullable=True,default=0)
@event.listens_for(UserProfileModel, "before_update", propagate=True)
def receive_before_update(mapper, connection, target):  
    target.modify_time = datetime.now()
@event.listens_for(UserProfileModel, "before_insert", propagate=True)
def receive_before_insert(mapper, connection, target):
    target.create_time = datetime.now() 
    target.modify_time = datetime.now()
