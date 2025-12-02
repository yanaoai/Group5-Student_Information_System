from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Table, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
import datetime
import enum

# --- 枚举定义 ---
class Role(str, enum.Enum):
    COURSE_DIRECTOR = "course_director"
    WELLBEING_OFFICER = "wellbeing_officer"

class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"

# --- 1. 关联表: 学生选课 (多对多) ---
student_courses = Table(
    'student_courses',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True)
)

# --- 2. 系统用户表 (仅限工作人员) ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    
    # 角色仅限: course_director 或 wellbeing_officer
    role = Column(SQLEnum(Role)) 

# --- 3. 学生表 (纯数据对象) ---
# 这是被管理的对象，包含学号、姓名等档案信息
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_number = Column(String, unique=True, index=True) # 例如: u1234567
    full_name = Column(String)
    email = Column(String, unique=True) # 仅用于记录联系方式

    # 关系: 学生的课程、成绩、出勤、健康记录
    enrolled_courses = relationship("Course", secondary=student_courses, back_populates="students")
    grades = relationship("Grade", back_populates="student")
    attendances = relationship("Attendance", back_populates="student")
    surveys = relationship("WellbeingSurvey", back_populates="student")

# --- 4. 课程表 (Courses) ---
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True)  # 例如: WM9QF
    name = Column(String)
    
    # 选修该课的学生
    students = relationship("Student", secondary=student_courses, back_populates="enrolled_courses")
    grades = relationship("Grade", back_populates="course")
    attendances = relationship("Attendance", back_populates="course")

# --- 5. 成绩表 (Grades) - 学术数据 ---
class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    
    assignment_title = Column(String)
    score = Column(Float)
    submission_date = Column(DateTime)
    
    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")

# --- 6. 出勤表 (Attendance) - 学术数据 ---
class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    
    date = Column(DateTime)
    status = Column(SQLEnum(AttendanceStatus))
    
    student = relationship("Student", back_populates="attendances")
    course = relationship("Course", back_populates="attendances")

# --- 7. 健康调查表 (Wellbeing) - 敏感数据 ---
# 只有 Wellbeing Officer 能访问此表
class WellbeingSurvey(Base):
    __tablename__ = "wellbeing_surveys"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    
    week_number = Column(Integer)
    stress_level = Column(Integer) # 1-5
    hours_slept = Column(Float)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    student = relationship("Student", back_populates="surveys")