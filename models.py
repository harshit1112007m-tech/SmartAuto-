"""
Database models for Faculty and Class Management System
"""
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass
from enum import Enum
import json

class UserRole(Enum):
    ADMIN = "admin"
    FACULTY = "faculty"
    STUDENT = "student"

class ClassStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    COMPLETED = "completed"

@dataclass
class User:
    id: int
    username: str
    email: str
    password_hash: str
    role: UserRole
    created_at: datetime
    is_active: bool = True

@dataclass
class Faculty:
    id: int
    user_id: int
    first_name: str
    last_name: str
    employee_id: str
    department: str
    specialization: str
    phone: str
    office_location: str
    hire_date: datetime
    salary: float
    is_active: bool = True

@dataclass
class Course:
    id: int
    course_code: str
    course_name: str
    description: str
    credits: int
    department: str
    prerequisites: List[str] = None

@dataclass
class Class:
    id: int
    class_code: str
    course_id: int
    faculty_id: int
    semester: str
    academic_year: str
    schedule: str  # e.g., "MWF 10:00-11:00"
    room: str
    max_capacity: int
    current_enrollment: int = 0
    status: ClassStatus = ClassStatus.ACTIVE
    created_at: datetime = None

@dataclass
class Student:
    id: int
    user_id: int
    first_name: str
    last_name: str
    student_id: str
    major: str
    year_level: int
    phone: str
    email: str
    enrollment_date: datetime
    is_active: bool = True

@dataclass
class Enrollment:
    id: int
    student_id: int
    class_id: int
    enrollment_date: datetime
    grade: Optional[str] = None
    status: str = "enrolled"  # enrolled, dropped, completed

@dataclass
class Attendance:
    id: int
    class_id: int
    student_id: int
    date: datetime
    status: str  # present, absent, late
    notes: Optional[str] = None