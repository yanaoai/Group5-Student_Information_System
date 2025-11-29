from pathlib import Path
import sys
from sqlalchemy import inspect

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from database import Base, engine
import create_db  # this should define create_database() and import models

def test_create_database_creates_all_core_tables():
    """
    DB setup test:
    - Drops any existing tables
    - Calls create_db.create_database()
    - Checks that all core tables exist
    """
    
    # Start from a clean schema
    Base.metadata.drop_all(bind=engine)

    # Call the function under test
    create_db.create_database()

    # Inspect the database schema
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())

    # These should be the __tablename__ values in your models.py
    expected_tables = {
        "students",
        "courses",
        "grades",
        "attendances",
        "wellbeing_surveys",
    }

    for name in expected_tables:
        assert name in table_names
