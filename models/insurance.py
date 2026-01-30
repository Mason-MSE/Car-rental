from decimal import Decimal
from sqlalchemy import (
    Column, Float, String, Integer, DateTime, Numeric, event, Date
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class InsuranceModel(Base):
    __tablename__ = 'insurance'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(Integer(), nullable=False)
    booking_id = Column(Integer(), nullable=False)

    insurance_type = Column(Integer(), nullable=False)
    policy_number = Column(String(64), nullable=False, unique=True)
    provider = Column(String(100), nullable=False)
    insurance_price_id=Column(Integer(),nullable=False)


    coverage_amount = Column(Numeric(12, 2), nullable=False)
    premium = Column(Numeric(10, 2), nullable=False)

    start_date = Column(Date(), nullable=False)
    end_date = Column(Date(), nullable=False)

    status = Column(Integer(), nullable=False, default=1)

    create_time = Column(DateTime(), nullable=True)
    modify_time = Column(DateTime(), nullable=True)

    is_deleted = Column(Integer(), nullable=False, default=0)

# @event.listens_for(InsuranceModel, "before_update", propagate=True)
# def receive_before_update(mapper, connection, target):
#     target.modify_time = datetime.now()


# @event.listens_for(InsuranceModel, "before_insert", propagate=True)
# def receive_before_insert(mapper, connection, target):
#     target.create_time = datetime.now()
#     target.modify_time = datetime.now()


Base = declarative_base()

class InsuranceCompanyModel(Base):
    __tablename__ = 'insurance_company'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    contact_email = Column(String(100))
    contact_phone = Column(String(50))
    status = Column(Integer(), default=1)
    create_time = Column(DateTime(), nullable=True)
    modify_time = Column(DateTime(), nullable=True)
    is_deleted = Column(Integer(),nullable=False, default=0)
# @event.listens_for(InsuranceCompanyModel, "before_update", propagate=True)
# def receive_before_update(mapper, connection, target):
#     target.modify_time = datetime.now()


# @event.listens_for(InsuranceCompanyModel, "before_insert", propagate=True)
# def receive_before_insert(mapper, connection, target):
#     target.create_time = datetime.now()
#     target.modify_time = datetime.now()
class InsuranceCatalogueModel(Base):
    __tablename__ = 'insurance_catalogue'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    description = Column(String(),nullable=True)
    company_id = Column(Integer(), nullable=False)
    insurance_type = Column(Integer(), nullable=False)
    status = Column(Integer(), default=1)
    create_time = Column(DateTime(), nullable=True)
    modify_time = Column(DateTime(), nullable=True)
    is_deleted = Column(Integer(),nullable=False,  default=0)


class InsurancePriceModel(Base):
    __tablename__ = 'insurance_price'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    catalogue_id = Column(Integer(),nullable=False)
    coverage_amount = Column(Float(), nullable=True)
    premium = Column(Float(), nullable=True)
    duration_days = Column(Integer(), nullable=False)
    status = Column(Integer(), default=1)
    create_time = Column(DateTime(), nullable=True)
    modify_time = Column(DateTime(), nullable=True)
    is_deleted = Column(Integer(),nullable=False,  default=0)

# @event.listens_for(InsurancePriceModel, "before_update", propagate=True)
# def receive_before_update(mapper, connection, target):
#     target.modify_time = datetime.now()


# @event.listens_for(InsurancePriceModel, "before_insert", propagate=True)
# def receive_before_insert(mapper, connection, target):
#     target.create_time = datetime.now()
#     target.modify_time = datetime.now()

for Model in [InsuranceModel,InsuranceCompanyModel, InsuranceCatalogueModel, InsurancePriceModel]:

    @event.listens_for(Model, "before_insert", propagate=True)
    def before_insert(mapper, connection, target):
        target.create_time = datetime.now()
        target.modify_time = datetime.now()

    @event.listens_for(Model, "before_update", propagate=True)
    def before_update(mapper, connection, target):
        target.modify_time = datetime.now()