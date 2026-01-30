# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Replace with your MySQL credentials
DB_USER = "root"
DB_PASSWORD = "rootpassword"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "rental"

# SQLAlchemy database URL for MySQL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,           # Shows SQL queries in the console
    pool_pre_ping=True   # Optional: checks connections before using
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class
class Base(DeclarativeBase):
    pass

# Dependency for FastAPI / function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
