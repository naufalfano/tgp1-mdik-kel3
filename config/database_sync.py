import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

Engine = create_engine(
    DATABASE_URL,
    pool_size=20,                # Maximum number of connections to keep in the pool
    max_overflow=10,             # Maximum number of connections to create beyond pool_size
    pool_timeout=30,             # Seconds to wait before timing out on getting a connection
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()