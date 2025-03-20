from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Initialize the database connection
filename = "Credentials.env"
load_dotenv(filename)

# Get the database URL
DATABASE_URL = f"postgresql+asyncpg://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/bookstore"

# Create the database engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Create the session
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Create the base class
Base = declarative_base()
