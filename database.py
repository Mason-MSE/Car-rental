# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from typing import Generator

# Declarative base class
class Base(DeclarativeBase):
    pass

# Database configuration dictionary
DATABASES = {
    "mysql": {
        "user": "root",
        "password": "rootpassword",
        "host": "127.0.0.1",
        "port": "3306",
        "db_name": "rental",
        "driver": "mysql+pymysql"
    },
    "sqlite": {
        "file": "rental.db",
        "driver": "sqlite"
    }
}

class DatabaseFactory:
    """
    Factory class to create SQLAlchemy engine and session.
    Supports multiple database types.
    """

    @staticmethod
    def create_engine_and_session(db_type: str = "mysql"):
        if db_type not in DATABASES:
            raise ValueError(f"Unsupported database type: {db_type}")

        config = DATABASES[db_type]

        if db_type == "mysql":
            url = f"{config['driver']}://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['db_name']}?charset=utf8mb4"
        elif db_type == "sqlite":
            url = f"{config['driver']}:///{config['file']}"
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

        engine = create_engine(
            url,
            echo=True,
            pool_pre_ping=True
        )

        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return engine, SessionLocal

# Example: create default MySQL engine and session
engine, SessionLocal = DatabaseFactory.create_engine_and_session("mysql")

# Dependency for FastAPI
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
