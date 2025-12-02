from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Where your SQLite database file will live
DATABASE_URL = "sqlite:///database.db"  # this file will be created in your project folder

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Session factory
SessionLocal = sessionmaker(bind=engine)

# Base class for your models to inherit from
Base = declarative_base()