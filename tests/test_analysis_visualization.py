from pathlib import Path
import sys
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from database import SessionLocal, Base, engine
import load_data
from models import Grade
from analysis_visualization import (
    generate_academic_statistics,
    generate_health_statistics,
    shapiro_wilk_normality_test,
)

def setup_module(module):
    """
    For this test module we:
    - Drop and recreate all tables
    - Call load_data.main() to load all CSV data
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    load_data.main()

def test_generate_health_statistics_returns_dataframe():
    session = SessionLocal()
    try:
        df_health = generate_health_statistics(session)

        # We know we have wellbeing_survey data, so this should not be None
        assert df_health is not None
        assert isinstance(df_health, pd.DataFrame)
        assert len(df_health) > 0

        # Check that key columns exist
        for col in ("week", "stress", "sleep", "student_id"):
            assert col in df_health.columns
    finally:
        session.close()

def test_generate_academic_statistics_handles_grades_safely():
    """
    With the current CSVs, grades may all be skipped because student/course
    ids in grades.csv don't match those in students.csv/courses.csv.
    This test only checks that the function behaves safely in both cases.
    """
    session = SessionLocal()
    try:
        grade_count = session.query(Grade).count()

        df_grades, df_attendance, normality_results = generate_academic_statistics(session)

        # normality_results should always be a dict
        assert isinstance(normality_results, dict)

        if grade_count == 0:
            # Current dataset case: no valid grades loaded
            assert df_grades is None
            assert df_attendance is None
        else:
            # Future-proof: if grades data is fixed, we still accept DataFrames
            assert isinstance(df_grades, pd.DataFrame)
            assert isinstance(df_attendance, pd.DataFrame)
            assert len(df_grades) > 0
    finally:
        session.close()

def test_shapiro_wilk_normality_test_output_types():
    scores = [50, 60, 70, 80, 90]

    is_normal, p_value = shapiro_wilk_normality_test(scores, "Test Course")

    assert isinstance(is_normal, bool)
    assert isinstance(p_value, float)
    assert 0.0 <= p_value <= 1.0
