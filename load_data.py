import csv
import datetime
from pathlib import Path
from database import SessionLocal
from models import (
    Student,
    Course,
    Grade,
    Attendance,
    WellbeingSurvey,
    AttendanceStatus,
)

# Folder where your CSV files live, e.g. Group5-Student_Information_System/data
DATA_DIR = Path(__file__).resolve().parent / "data"

def parse_iso_datetime(value: str) -> datetime.datetime:
    """
    Parse strings like '2025-11-14T00:00:00' or '2025-11-17 10:00:00'
    into a datetime object.
    """
    return datetime.datetime.fromisoformat(value)

def load_students(session, filename: str = "students.csv") -> None:
    path = DATA_DIR / filename
    print(f"Loading students from {path} ...")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Use the CSV id as our primary key so it matches student_id
            student = Student(
                id=int(row["id"]),
                student_number=row["student_number"],
                full_name=row["full_name"],
                email=row["email"],
            )
            session.add(student)

    session.commit()
    print("Students loaded.")

def load_courses(session, filename: str = "courses.csv") -> None:
    path = DATA_DIR / filename
    print(f"Loading courses from {path} ...")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            course = Course(
                id=int(row["id"]),
                code=row["code"],
                name=row["name"],
            )
            session.add(course)

    session.commit()
    print("Courses loaded.")

def build_lookup_maps(session):
    """
    Build helper dicts:
    - student_number (like 'u5705711') -> student.id (int)   [for grades.csv]
    - course_code (like 'WM450') -> course.id (int)
    """
    students = session.query(Student).all()
    courses = session.query(Course).all()

    student_map = {s.student_number: s.id for s in students}
    course_map = {c.code: c.id for c in courses}

    print(f"Student map size: {len(student_map)}")
    print(f"Course map size: {len(course_map)}")

    return student_map, course_map

def load_attendance(session, course_map, filename: str = "attendance_time.csv") -> None:
    path = DATA_DIR / filename
    print(f"Loading attendance from {path} ...")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # New file: student_id is an integer matching students.id
            student_id = int(row["student_id"])
            course_code = row["course_id"]
            status_val = row["status"]

            course_id = course_map.get(course_code)
            if course_id is None:
                print(f"Skipping attendance row, unknown course: {row}")
                continue

            # Map status value to AttendanceStatus enum
            if status_val == "1":
                status = AttendanceStatus.PRESENT
            elif status_val == "2":
                status = AttendanceStatus.LATE
            else:
                status = AttendanceStatus.ABSENT

            attendance = Attendance(
                student_id=student_id,
                course_id=course_id,
                date=parse_iso_datetime(row["date"]),
                status=status,
            )
            session.add(attendance)

    session.commit()
    print("Attendance loaded.")

def load_grades(
    session,
    student_map,
    course_map,
    filename: str = "grades.csv",
) -> None:
    path = DATA_DIR / filename
    print(f"Loading grades from {path} ...")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # grades.csv: student_id is still the u-number (e.g. 'u5705711')
            student_number = row["student_id"]
            course_code = row["course_id"]

            student_id = student_map.get(student_number)
            course_id = course_map.get(course_code)

            if student_id is None or course_id is None:
                print(f"Skipping grade row, unknown student/course: {row}")
                continue

            grade = Grade(
                student_id=student_id,
                course_id=course_id,
                assignment_title=row["assignment_title"],
                score=float(row["score"]),
                submission_date=parse_iso_datetime(row["submission_date"]),
            )
            session.add(grade)

    session.commit()
    print("Grades loaded.")

def load_wellbeing(session, filename: str = "wellbeing_survey.csv") -> None:
    path = DATA_DIR / filename
    print(f"Loading wellbeing surveys from {path} ...")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # wellbeing_survey.csv: student_id is an integer matching students.id
            survey = WellbeingSurvey(
                student_id=int(row["student_id"]),
                week_number=int(row["week_number"]),
                stress_level=int(row["stress_level"]),
                hours_slept=float(row["hours_slept"]),
                recorded_at=parse_iso_datetime(row["recorded_at"]),
            )
            session.add(survey)

    session.commit()
    print("Wellbeing surveys loaded.")

def main():
    session = SessionLocal()
    try:
        # 1. Basic reference data
        load_students(session)
        load_courses(session)

        # 2. Build lookup dicts for grades (u-number & course code)
        student_map, course_map = build_lookup_maps(session)

        # 3. Load dependent data
        load_attendance(session, course_map)
        load_grades(session, student_map, course_map)
        load_wellbeing(session)

        print("All data loaded successfully into your database file.")

    finally:
        session.close()

if __name__ == "__main__":
    main()
