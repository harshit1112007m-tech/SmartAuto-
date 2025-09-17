"""
Database operations for Faculty and Class Management System
"""
import sqlite3
import hashlib
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from models import *

class DatabaseManager:
    def __init__(self, db_path: str = "faculty_management.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Faculty table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS faculty (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                employee_id TEXT UNIQUE NOT NULL,
                department TEXT NOT NULL,
                specialization TEXT NOT NULL,
                phone TEXT NOT NULL,
                office_location TEXT NOT NULL,
                hire_date TIMESTAMP NOT NULL,
                salary REAL NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Courses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_code TEXT UNIQUE NOT NULL,
                course_name TEXT NOT NULL,
                description TEXT,
                credits INTEGER NOT NULL,
                department TEXT NOT NULL,
                prerequisites TEXT DEFAULT '[]'
            )
        ''')
        
        # Classes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_code TEXT UNIQUE NOT NULL,
                course_id INTEGER NOT NULL,
                faculty_id INTEGER NOT NULL,
                semester TEXT NOT NULL,
                academic_year TEXT NOT NULL,
                schedule TEXT NOT NULL,
                room TEXT NOT NULL,
                max_capacity INTEGER NOT NULL,
                current_enrollment INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses (id),
                FOREIGN KEY (faculty_id) REFERENCES faculty (id)
            )
        ''')
        
        # Students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                student_id TEXT UNIQUE NOT NULL,
                major TEXT NOT NULL,
                year_level INTEGER NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                enrollment_date TIMESTAMP NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Enrollments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                class_id INTEGER NOT NULL,
                enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                grade TEXT,
                status TEXT DEFAULT 'enrolled',
                FOREIGN KEY (student_id) REFERENCES students (id),
                FOREIGN KEY (class_id) REFERENCES classes (id),
                UNIQUE(student_id, class_id)
            )
        ''')
        
        # Attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                date TIMESTAMP NOT NULL,
                status TEXT NOT NULL,
                notes TEXT,
                FOREIGN KEY (class_id) REFERENCES classes (id),
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return self.hash_password(password) == hashed

    # User operations
    def create_user(self, username: str, email: str, password: str, role: UserRole) -> int:
        """Create a new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, role.value))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user login"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, password_hash, role, created_at, is_active
            FROM users WHERE username = ? AND is_active = 1
        ''', (username,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row and self.verify_password(password, row[3]):
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                password_hash=row[3],
                role=UserRole(row[4]),
                created_at=datetime.fromisoformat(row[5]),
                is_active=bool(row[6])
            )
        return None

    # Faculty operations
    def create_faculty(self, user_id: int, first_name: str, last_name: str, 
                      employee_id: str, department: str, specialization: str,
                      phone: str, office_location: str, hire_date: datetime, salary: float) -> int:
        """Create a new faculty member"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO faculty (user_id, first_name, last_name, employee_id, 
                               department, specialization, phone, office_location, 
                               hire_date, salary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, first_name, last_name, employee_id, department, 
              specialization, phone, office_location, hire_date, salary))
        
        faculty_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return faculty_id

    def get_all_faculty(self) -> List[Faculty]:
        """Get all faculty members"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, user_id, first_name, last_name, employee_id, department,
                   specialization, phone, office_location, hire_date, salary, is_active
            FROM faculty WHERE is_active = 1
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [Faculty(
            id=row[0], user_id=row[1], first_name=row[2], last_name=row[3],
            employee_id=row[4], department=row[5], specialization=row[6],
            phone=row[7], office_location=row[8], hire_date=datetime.fromisoformat(row[9]),
            salary=row[10], is_active=bool(row[11])
        ) for row in rows]

    def get_faculty_by_id(self, faculty_id: int) -> Optional[Faculty]:
        """Get faculty by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, user_id, first_name, last_name, employee_id, department,
                   specialization, phone, office_location, hire_date, salary, is_active
            FROM faculty WHERE id = ? AND is_active = 1
        ''', (faculty_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Faculty(
                id=row[0], user_id=row[1], first_name=row[2], last_name=row[3],
                employee_id=row[4], department=row[5], specialization=row[6],
                phone=row[7], office_location=row[8], hire_date=datetime.fromisoformat(row[9]),
                salary=row[10], is_active=bool(row[11])
            )
        return None

    def update_faculty(self, faculty_id: int, **kwargs) -> bool:
        """Update faculty information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build dynamic update query
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [faculty_id]
        
        cursor.execute(f'''
            UPDATE faculty SET {set_clause} WHERE id = ?
        ''', values)
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def deactivate_faculty(self, faculty_id: int) -> bool:
        """Deactivate faculty member"""
        return self.update_faculty(faculty_id, is_active=False)

    # Course operations
    def create_course(self, course_code: str, course_name: str, description: str,
                     credits: int, department: str, prerequisites: List[str] = None) -> int:
        """Create a new course"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        prerequisites_json = json.dumps(prerequisites or [])
        cursor.execute('''
            INSERT INTO courses (course_code, course_name, description, credits, department, prerequisites)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (course_code, course_name, description, credits, department, prerequisites_json))
        
        course_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return course_id

    def get_all_courses(self) -> List[Course]:
        """Get all courses"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, course_code, course_name, description, credits, department, prerequisites
            FROM courses
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [Course(
            id=row[0], course_code=row[1], course_name=row[2], description=row[3],
            credits=row[4], department=row[5], prerequisites=json.loads(row[6] or '[]')
        ) for row in rows]

    # Class operations
    def create_class(self, class_code: str, course_id: int, faculty_id: int,
                    semester: str, academic_year: str, schedule: str, room: str,
                    max_capacity: int) -> int:
        """Create a new class"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO classes (class_code, course_id, faculty_id, semester, 
                               academic_year, schedule, room, max_capacity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (class_code, course_id, faculty_id, semester, academic_year, 
              schedule, room, max_capacity))
        
        class_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return class_id

    def get_all_classes(self) -> List[Class]:
        """Get all classes with course and faculty information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.id, c.class_code, c.course_id, c.faculty_id, c.semester,
                   c.academic_year, c.schedule, c.room, c.max_capacity, c.current_enrollment,
                   c.status, c.created_at, co.course_name, f.first_name, f.last_name
            FROM classes c
            JOIN courses co ON c.course_id = co.id
            JOIN faculty f ON c.faculty_id = f.id
            ORDER BY c.academic_year DESC, c.semester
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        classes = []
        for row in rows:
            class_obj = Class(
                id=row[0], class_code=row[1], course_id=row[2], faculty_id=row[3],
                semester=row[4], academic_year=row[5], schedule=row[6], room=row[7],
                max_capacity=row[8], current_enrollment=row[9], 
                status=ClassStatus(row[10]), created_at=datetime.fromisoformat(row[11])
            )
            # Add course and faculty names for display
            class_obj.course_name = row[12]
            class_obj.faculty_name = f"{row[13]} {row[14]}"
            classes.append(class_obj)
        
        return classes

    def get_class_by_id(self, class_id: int) -> Optional[Class]:
        """Get class by ID with course and faculty information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.id, c.class_code, c.course_id, c.faculty_id, c.semester,
                   c.academic_year, c.schedule, c.room, c.max_capacity, c.current_enrollment,
                   c.status, c.created_at, co.course_name, f.first_name, f.last_name
            FROM classes c
            JOIN courses co ON c.course_id = co.id
            JOIN faculty f ON c.faculty_id = f.id
            WHERE c.id = ?
        ''', (class_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            class_obj = Class(
                id=row[0], class_code=row[1], course_id=row[2], faculty_id=row[3],
                semester=row[4], academic_year=row[5], schedule=row[6], room=row[7],
                max_capacity=row[8], current_enrollment=row[9], 
                status=ClassStatus(row[10]), created_at=datetime.fromisoformat(row[11])
            )
            class_obj.course_name = row[12]
            class_obj.faculty_name = f"{row[13]} {row[14]}"
            return class_obj
        return None

    def update_class(self, class_id: int, **kwargs) -> bool:
        """Update class information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [class_id]
        
        cursor.execute(f'''
            UPDATE classes SET {set_clause} WHERE id = ?
        ''', values)
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    # Student operations
    def create_student(self, user_id: int, first_name: str, last_name: str,
                      student_id: str, major: str, year_level: int, phone: str,
                      email: str, enrollment_date: datetime) -> int:
        """Create a new student"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO students (user_id, first_name, last_name, student_id, 
                               major, year_level, phone, email, enrollment_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, first_name, last_name, student_id, major, year_level, 
              phone, email, enrollment_date))
        
        student_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return student_id

    def get_all_students(self) -> List[Student]:
        """Get all students"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, user_id, first_name, last_name, student_id, major, 
                   year_level, phone, email, enrollment_date, is_active
            FROM students WHERE is_active = 1
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [Student(
            id=row[0], user_id=row[1], first_name=row[2], last_name=row[3],
            student_id=row[4], major=row[5], year_level=row[6], phone=row[7],
            email=row[8], enrollment_date=datetime.fromisoformat(row[9]), 
            is_active=bool(row[10])
        ) for row in rows]

    # Enrollment operations
    def enroll_student(self, student_id: int, class_id: int) -> bool:
        """Enroll student in a class"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if class has capacity
            cursor.execute('SELECT max_capacity, current_enrollment FROM classes WHERE id = ?', (class_id,))
            row = cursor.fetchone()
            if not row or row[1] >= row[0]:
                return False
            
            # Enroll student
            cursor.execute('''
                INSERT INTO enrollments (student_id, class_id)
                VALUES (?, ?)
            ''', (student_id, class_id))
            
            # Update enrollment count
            cursor.execute('''
                UPDATE classes SET current_enrollment = current_enrollment + 1
                WHERE id = ?
            ''', (class_id,))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Student already enrolled
            return False
        finally:
            conn.close()

    def get_class_enrollments(self, class_id: int) -> List[Dict]:
        """Get all enrollments for a class"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT e.id, s.student_id, s.first_name, s.last_name, s.major, 
                   s.year_level, e.enrollment_date, e.grade, e.status
            FROM enrollments e
            JOIN students s ON e.student_id = s.id
            WHERE e.class_id = ? AND s.is_active = 1
        ''', (class_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'enrollment_id': row[0],
            'student_id': row[1],
            'name': f"{row[2]} {row[3]}",
            'major': row[4],
            'year_level': row[5],
            'enrollment_date': row[6],
            'grade': row[7],
            'status': row[8]
        } for row in rows]

    def drop_student(self, student_id: int, class_id: int) -> bool:
        """Drop student from a class"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Remove enrollment
            cursor.execute('''
                DELETE FROM enrollments WHERE student_id = ? AND class_id = ?
            ''', (student_id, class_id))
            
            if cursor.rowcount > 0:
                # Update enrollment count
                cursor.execute('''
                    UPDATE classes SET current_enrollment = current_enrollment - 1
                    WHERE id = ?
                ''', (class_id,))
                conn.commit()
                return True
            return False
        finally:
            conn.close()

    # Analytics and reporting
    def get_faculty_workload(self, faculty_id: int) -> Dict:
        """Get faculty workload statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) as total_classes, 
                   SUM(current_enrollment) as total_students,
                   AVG(current_enrollment) as avg_class_size
            FROM classes 
            WHERE faculty_id = ? AND status = 'active'
        ''', (faculty_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return {
            'total_classes': row[0] or 0,
            'total_students': row[1] or 0,
            'avg_class_size': round(row[2] or 0, 2)
        }

    def get_department_statistics(self) -> Dict:
        """Get department statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT f.department, COUNT(DISTINCT f.id) as faculty_count,
                   COUNT(DISTINCT c.id) as class_count,
                   SUM(c.current_enrollment) as total_enrollment
            FROM faculty f
            LEFT JOIN classes c ON f.id = c.faculty_id AND c.status = 'active'
            WHERE f.is_active = 1
            GROUP BY f.department
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'department': row[0],
            'faculty_count': row[1],
            'class_count': row[2] or 0,
            'total_enrollment': row[3] or 0
        } for row in rows]