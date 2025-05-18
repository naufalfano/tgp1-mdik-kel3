import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

Engine = create_async_engine(
    DATABASE_URL,
    pool_size=50,
    max_overflow=50,
)

AsyncSessionLocal = sessionmaker(
    bind=Engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
