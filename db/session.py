from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from core.config import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL   # Retrieve  db_urlfrom configuration settings
engine = create_engine(SQLALCHEMY_DATABASE_URL)   # SQLAlchemy engine creation using specified db_url
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)    # configuring session behavior

# function to get a database session
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()