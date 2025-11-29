import datetime
from load_data import parse_iso_datetime
from database import SessionLocal
from models import Student, Course, Attendance, Grade, WellbeingSurvey
import create_db
import load_data

def test_parse_iso_datetime_returns_datetime():
    value = "2025-11-14T00:00:00"
    result = parse_iso_datetime(value)

    assert isinstance(result, datetime.datetime)
    assert result.year == 2025
    assert result.month == 11
    assert result.day == 14

def setup_module(module):
    """
    Prepare a fresh database for these tests:
    - create tables
    - load CSV data once
    """
    # You will get duplicate-key errors if the DB already has data.
    # Easiest: delete the .db file before running pytest.
    create_db.create_database()
    load_data.main()

def test_students_loaded():
    session = SessionLocal()
    try:
        count = session.query(Student).count()
        # We know students.csv has 80 rows
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
