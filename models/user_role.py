from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Numeric, event,Date,Time
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class UserRoleModel(Base):
    __tablename__ = 'user_role'

    user_id = Column(Integer(), primary_key=True)
    role_id = Column(Integer(), primary_key=True)
    create_time = Column(DateTime(), nullable=True)
    modify_time = Column(DateTime(), nullable=True)
    is_deleted = Column(Integer(), nullable=True, default=0)
@event.listens_for(UserRoleModel, "before_update", propagate=True)
def receive_before_update(mapper, connection, target):  
    target.modify_time = datetime.now()
@event.listens_for(UserRoleModel, "before_insert", propagate=True)
def receive_before_insert(mapper, connection, target):
    target.create_time = datetime.now() 
    target.modify_time = datetime.now()
