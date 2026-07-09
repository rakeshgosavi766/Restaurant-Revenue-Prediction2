import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Render वर DATABASE_URL Environment Variable मधून घे
DATABASE_URL = os.getenv("DATABASE_URL")

# Local वर चालवायचं असल्यास fallback
if DATABASE_URL is None:
    DATABASE_URL = "postgresql://postgres:Admin@localhost:5432/ml_database"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
