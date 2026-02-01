from sqlalchemy import Column, Integer, Float, DateTime, event
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class RealTimeLocationModel(Base):
    __tablename__ = 'real_time_location'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    car_id = Column(Integer(), nullable=False, index=True)
    latitude = Column(Float(precision=7), nullable=False)
    longitude = Column(Float(precision=7), nullable=False)
    speed = Column(Float(precision=2), nullable=True, default=0.0)         # km/h
    heading = Column(Float(precision=2), nullable=True, default=0.0)       # 0-360 degrees
    status = Column(Integer(), nullable=True, default=1)                    # 0=idle,1=active,2=offline
    timestamp = Column(DateTime(), nullable=False, default=datetime.now)    # recorded time
    create_time = Column(DateTime(), nullable=True)
    modify_time = Column(DateTime(), nullable=True)
    is_deleted = Column(Integer(), nullable=True, default=0)

# -------------------------
# Event listeners for timestamps
# -------------------------
@event.listens_for(RealTimeLocationModel, "before_insert", propagate=True)
def receive_before_insert(mapper, connection, target):
    """Set create_time and modify_time on insert"""
    now = datetime.now()
    target.create_time = now
    target.modify_time = now

@event.listens_for(RealTimeLocationModel, "before_update", propagate=True)
def receive_before_update(mapper, connection, target):
    """Update modify_time on update"""
    target.modify_time = datetime.now()
