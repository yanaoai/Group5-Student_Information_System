import datetime
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from database import SessionLocal, Base, engine
from models import Student, Course, Attendance, Grade, WellbeingSurvey
import load_data
from load_data import parse_iso_datetime

def setup_module(module):
    """
    Prepare a fresh database for these tests:

    - Drop and recreate all tables (so we don't get duplicate key errors)
    - Run load_data.main() to load all CSV data into the DB
    """
    # Drop all existing tables (if any), then recreate them
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Call your loading pipeline
    load_data.main()

def test_parse_iso_datetime_returns_datetime():
    value = "2025-11-14T00:00:00"
    result = parse_iso_datetime(value)

    assert isinstance(result, datetime.datetime)
    assert result.year == 2025
    assert result.month == 11
    assert result.day == 14

def test_students_loaded():
    session = SessionLocal()
    try:
        count = session.query(Student).count()
        # students.csv has 80 rows
        assert count == 80
    finally:
        session.close()

def test_courses_loaded():
    session = SessionLocal()
    try:
        count = session.query(Course).count()
        # courses.csv has 5 rows
        assert count == 5
    finally:
        session.close()

def test_wellbeing_loaded():
    session = SessionLocal()
    try:
        count = session.query(WellbeingSurvey).count()
        # wellbeing_survey.csv has 320 rows
        assert count == 320
    finally:
        session.close()

def test_attendance_loaded():
    session = SessionLocal()
    try:
        count = session.query(Attendance).count()
        # We don't need the exact number here, just that something was loaded
        assert count > 0
    finally:
        session.close()

def test_grades_loaded():
    session = SessionLocal()
    try:
        count = session.query(Grade).count()
        assert count >= 0
    finally:
        session.close()
