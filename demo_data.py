"""
Demo data generator for Faculty and Class Management System
This script populates the database with sample data for testing and demonstration
"""
from datetime import datetime, timedelta
from database import DatabaseManager
from models import UserRole

def create_demo_data():
    """Create sample data for demonstration purposes"""
    db = DatabaseManager()
    
    print("Creating demo data...")
    
    # Create demo courses
    courses_data = [
        ("CS101", "Introduction to Computer Science", "Basic programming concepts", 3, "Computer Science", []),
        ("CS201", "Data Structures", "Advanced programming and data structures", 3, "Computer Science", ["CS101"]),
        ("CS301", "Algorithms", "Algorithm design and analysis", 3, "Computer Science", ["CS201"]),
        ("MATH101", "Calculus I", "Differential calculus", 4, "Mathematics", []),
        ("MATH201", "Calculus II", "Integral calculus", 4, "Mathematics", ["MATH101"]),
        ("PHYS101", "Physics I", "Mechanics and thermodynamics", 4, "Physics", []),
        ("PHYS201", "Physics II", "Electricity and magnetism", 4, "Physics", ["PHYS101"]),
        ("ENG101", "English Composition", "Writing and communication skills", 3, "English", []),
        ("HIST101", "World History", "Survey of world history", 3, "History", []),
        ("CHEM101", "General Chemistry", "Basic chemistry principles", 4, "Chemistry", [])
    ]
    
    course_ids = []
    for course_data in courses_data:
        course_id = db.create_course(*course_data)
        course_ids.append(course_id)
        print(f"Created course: {course_data[0]} - {course_data[1]}")
    
    # Create demo faculty
    faculty_data = [
        ("john_doe", "john.doe@university.edu", "password123", "John", "Doe", "F001", "Computer Science", "Software Engineering", "555-0101", "CS Building Room 101", datetime.now() - timedelta(days=365*5), 75000),
        ("jane_smith", "jane.smith@university.edu", "password123", "Jane", "Smith", "F002", "Mathematics", "Applied Mathematics", "555-0102", "Math Building Room 201", datetime.now() - timedelta(days=365*3), 70000),
        ("bob_wilson", "bob.wilson@university.edu", "password123", "Bob", "Wilson", "F003", "Physics", "Quantum Physics", "555-0103", "Physics Building Room 301", datetime.now() - timedelta(days=365*7), 80000),
        ("alice_brown", "alice.brown@university.edu", "password123", "Alice", "Brown", "F004", "English", "Literature", "555-0104", "English Building Room 401", datetime.now() - timedelta(days=365*4), 65000),
        ("charlie_davis", "charlie.davis@university.edu", "password123", "Charlie", "Davis", "F005", "History", "American History", "555-0105", "History Building Room 501", datetime.now() - timedelta(days=365*6), 68000),
        ("diana_garcia", "diana.garcia@university.edu", "password123", "Diana", "Garcia", "F006", "Chemistry", "Organic Chemistry", "555-0106", "Chemistry Building Room 601", datetime.now() - timedelta(days=365*2), 72000)
    ]
    
    faculty_ids = []
    for faculty_data_item in faculty_data:
        user_id = db.create_faculty_user(faculty_data_item[0], faculty_data_item[1], faculty_data_item[2])
        faculty_id = db.create_faculty(
            user_id=user_id,
            first_name=faculty_data_item[3],
            last_name=faculty_data_item[4],
            employee_id=faculty_data_item[5],
            department=faculty_data_item[6],
            specialization=faculty_data_item[7],
            phone=faculty_data_item[8],
            office_location=faculty_data_item[9],
            hire_date=faculty_data_item[10],
            salary=faculty_data_item[11]
        )
        faculty_ids.append(faculty_id)
        print(f"Created faculty: {faculty_data_item[3]} {faculty_data_item[4]} - {faculty_data_item[6]}")
    
    # Create demo students
    students_data = [
        ("student1", "student1@university.edu", "password123", "Alice", "Johnson", "S001", "Computer Science", 1, "555-1001", datetime.now() - timedelta(days=30)),
        ("student2", "student2@university.edu", "password123", "Bob", "Williams", "S002", "Computer Science", 2, "555-1002", datetime.now() - timedelta(days=60)),
        ("student3", "student3@university.edu", "password123", "Carol", "Jones", "S003", "Mathematics", 1, "555-1003", datetime.now() - timedelta(days=45)),
        ("student4", "student4@university.edu", "password123", "David", "Brown", "S004", "Physics", 3, "555-1004", datetime.now() - timedelta(days=90)),
        ("student5", "student5@university.edu", "password123", "Eve", "Davis", "S005", "English", 2, "555-1005", datetime.now() - timedelta(days=75)),
        ("student6", "student6@university.edu", "password123", "Frank", "Miller", "S006", "History", 4, "555-1006", datetime.now() - timedelta(days=120)),
        ("student7", "student7@university.edu", "password123", "Grace", "Wilson", "S007", "Chemistry", 1, "555-1007", datetime.now() - timedelta(days=15)),
        ("student8", "student8@university.edu", "password123", "Henry", "Moore", "S008", "Computer Science", 3, "555-1008", datetime.now() - timedelta(days=105)),
        ("student9", "student9@university.edu", "password123", "Ivy", "Taylor", "S009", "Mathematics", 2, "555-1009", datetime.now() - timedelta(days=60)),
        ("student10", "student10@university.edu", "password123", "Jack", "Anderson", "S010", "Physics", 4, "555-1010", datetime.now() - timedelta(days=135))
    ]
    
    student_ids = []
    for student_data in students_data:
        user_id = db.create_student_user(student_data[0], student_data[1], student_data[2])
        student_id = db.create_student(
            user_id=user_id,
            first_name=student_data[3],
            last_name=student_data[4],
            student_id=student_data[5],
            major=student_data[6],
            year_level=student_data[7],
            phone=student_data[8],
            email=student_data[1],
            enrollment_date=student_data[9]
        )
        student_ids.append(student_id)
        print(f"Created student: {student_data[3]} {student_data[4]} - {student_data[6]}")
    
    # Create demo classes
    classes_data = [
        ("CS101-001", 0, 0, "Fall", "2024", "MWF 09:00-10:00", "CS-101", 30),  # CS101, John Doe
        ("CS101-002", 0, 0, "Fall", "2024", "MWF 11:00-12:00", "CS-102", 30),  # CS101, John Doe
        ("CS201-001", 1, 0, "Fall", "2024", "TTH 10:00-11:30", "CS-201", 25),  # CS201, John Doe
        ("MATH101-001", 3, 1, "Fall", "2024", "MWF 08:00-09:00", "MATH-101", 35),  # MATH101, Jane Smith
        ("MATH201-001", 4, 1, "Fall", "2024", "TTH 09:00-10:30", "MATH-201", 30),  # MATH201, Jane Smith
        ("PHYS101-001", 5, 2, "Fall", "2024", "MWF 10:00-11:00", "PHYS-101", 40),  # PHYS101, Bob Wilson
        ("PHYS201-001", 6, 2, "Fall", "2024", "TTH 11:00-12:30", "PHYS-201", 35),  # PHYS201, Bob Wilson
        ("ENG101-001", 7, 3, "Fall", "2024", "MWF 13:00-14:00", "ENG-101", 30),  # ENG101, Alice Brown
        ("HIST101-001", 8, 4, "Fall", "2024", "TTH 14:00-15:30", "HIST-101", 25),  # HIST101, Charlie Davis
        ("CHEM101-001", 9, 5, "Fall", "2024", "MWF 15:00-16:00", "CHEM-101", 30)   # CHEM101, Diana Garcia
    ]
    
    class_ids = []
    for i, class_data in enumerate(classes_data):
        class_id = db.create_class(
            class_code=class_data[0],
            course_id=course_ids[class_data[1]],
            faculty_id=faculty_ids[class_data[2]],
            semester=class_data[3],
            academic_year=class_data[4],
            schedule=class_data[5],
            room=class_data[6],
            max_capacity=class_data[7]
        )
        class_ids.append(class_id)
        print(f"Created class: {class_data[0]} - {courses_data[class_data[1]][1]}")
    
    # Create some enrollments
    enrollments = [
        (0, 0), (0, 1), (0, 2),  # Alice Johnson in CS101-001, CS101-002, CS201-001
        (1, 0), (1, 2),           # Bob Williams in CS101-001, CS201-001
        (2, 3), (2, 4),           # Carol Jones in MATH101-001, MATH201-001
        (3, 5), (3, 6),           # David Brown in PHYS101-001, PHYS201-001
        (4, 7),                   # Eve Davis in ENG101-001
        (5, 8),                   # Frank Miller in HIST101-001
        (6, 9),                   # Grace Wilson in CHEM101-001
        (7, 0), (7, 2),           # Henry Moore in CS101-001, CS201-001
        (8, 3), (8, 4),           # Ivy Taylor in MATH101-001, MATH201-001
        (9, 5), (9, 6)            # Jack Anderson in PHYS101-001, PHYS201-001
    ]
    
    for student_idx, class_idx in enrollments:
        db.enroll_student(student_ids[student_idx], class_ids[class_idx])
        print(f"Enrolled {students_data[student_idx][3]} {students_data[student_idx][4]} in {classes_data[class_idx][0]}")
    
    print("\nDemo data creation completed!")
    print(f"Created {len(course_ids)} courses, {len(faculty_ids)} faculty, {len(student_ids)} students, {len(class_ids)} classes")
    print(f"Created {len(enrollments)} enrollments")
    print("\nYou can now run the main application with: python main.py")
    print("Use the demo credentials to login as faculty or students.")

if __name__ == "__main__":
    create_demo_data()