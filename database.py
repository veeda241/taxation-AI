from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from . import db_models
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database URL from environment variable
SQLALCHEMY_DATABASE_URL = os.getenv("MYSQL_URL")


# Set up the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for models to inherit from
Base = declarative_base()

def get_db() -> Session:
    """
    Dependency that returns a new database session.
    This function should be used in route functions with the `Depends` keyword.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
