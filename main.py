"""
Main Application Interface for Faculty and Class Management System
"""
import os
import sys
from datetime import datetime
from database import DatabaseManager
from auth import AuthenticationManager
from faculty_manager import FacultyManager
from class_manager import ClassManager
from student_manager import StudentManager

class FacultyClassManagementSystem:
    def __init__(self):
        self.db = DatabaseManager()
        self.auth = AuthenticationManager(self.db)
        self.faculty_manager = FacultyManager(self.db, self.auth)
        self.class_manager = ClassManager(self.db, self.auth)
        self.student_manager = StudentManager(self.db, self.auth)
        self.running = True

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_header(self, title: str):
        """Display application header"""
        self.clear_screen()
        print("=" * 60)
        print(f"  {title}")
        print("=" * 60)

    def display_menu(self, menu_items: list, title: str = "Menu"):
        """Display a menu and get user choice"""
        print(f"\n{title}:")
        print("-" * 40)
        for i, item in enumerate(menu_items, 1):
            print(f"{i}. {item}")
        print("0. Exit/Back")
        
        while True:
            try:
                choice = int(input(f"\nEnter your choice (0-{len(menu_items)}): "))
                if 0 <= choice <= len(menu_items):
                    return choice
                else:
                    print(f"Please enter a number between 0 and {len(menu_items)}")
            except ValueError:
                print("Please enter a valid number")

    def login_menu(self):
        """Display login menu"""
        self.display_header("Faculty & Class Management System - Login")
        
        while True:
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            if self.auth.login(username, password):
                print(f"\nWelcome, {self.auth.get_current_user().username}!")
                input("Press Enter to continue...")
                return True
            else:
                print("\nInvalid username or password. Please try again.")
                retry = input("Try again? (y/n): ").lower()
                if retry != 'y':
                    return False

    def admin_menu(self):
        """Admin main menu"""
        while True:
            self.display_header("Admin Dashboard")
            menu_items = [
                "Faculty Management",
                "Class Management", 
                "Student Management",
                "Reports & Analytics",
                "System Settings"
            ]
            
            choice = self.display_menu(menu_items, "Admin Menu")
            
            if choice == 0:
                break
            elif choice == 1:
                self.faculty_management_menu()
            elif choice == 2:
                self.class_management_menu()
            elif choice == 3:
                self.student_management_menu()
            elif choice == 4:
                self.reports_menu()
            elif choice == 5:
                self.system_settings_menu()

    def faculty_management_menu(self):
        """Faculty management submenu"""
        while True:
            self.display_header("Faculty Management")
            menu_items = [
                "Add New Faculty",
                "View All Faculty",
                "Search Faculty",
                "Update Faculty Information",
                "Deactivate Faculty",
                "Faculty Workload Report",
                "Export Faculty Data"
            ]
            
            choice = self.display_menu(menu_items, "Faculty Management")
            
            if choice == 0:
                break
            elif choice == 1:
                self.add_faculty()
            elif choice == 2:
                self.view_all_faculty()
            elif choice == 3:
                self.search_faculty()
            elif choice == 4:
                self.update_faculty()
            elif choice == 5:
                self.deactivate_faculty()
            elif choice == 6:
                self.faculty_workload_report()
            elif choice == 7:
                self.export_faculty_data()

    def add_faculty(self):
        """Add new faculty member"""
        self.display_header("Add New Faculty Member")
        
        print("Enter faculty information:")
        username = input("Username: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        employee_id = input("Employee ID: ").strip()
        department = input("Department: ").strip()
        specialization = input("Specialization: ").strip()
        phone = input("Phone: ").strip()
        office_location = input("Office Location: ").strip()
        
        try:
            salary = float(input("Salary: "))
            hire_date = datetime.now()
        except ValueError:
            print("Invalid salary amount")
            input("Press Enter to continue...")
            return
        
        result = self.faculty_manager.add_faculty(
            username, email, password, first_name, last_name,
            employee_id, department, specialization, phone,
            office_location, hire_date, salary
        )
        
        print(f"\n{result['message']}")
        input("Press Enter to continue...")

    def view_all_faculty(self):
        """View all faculty members"""
        self.display_header("All Faculty Members")
        
        faculty_list = self.faculty_manager.get_all_faculty()
        
        if not faculty_list:
            print("No faculty members found.")
        else:
            print(f"{'ID':<5} {'Name':<25} {'Department':<15} {'Specialization':<20} {'Phone':<15}")
            print("-" * 80)
            
            for faculty in faculty_list:
                name = f"{faculty.first_name} {faculty.last_name}"
                print(f"{faculty.id:<5} {name:<25} {faculty.department:<15} {faculty.specialization:<20} {faculty.phone:<15}")
        
        input("\nPress Enter to continue...")

    def search_faculty(self):
        """Search faculty members"""
        self.display_header("Search Faculty")
        
        search_term = input("Enter search term (name, department, specialization): ").strip()
        
        if not search_term:
            print("Search term cannot be empty.")
            input("Press Enter to continue...")
            return
        
        results = self.faculty_manager.search_faculty(search_term)
        
        if not results:
            print("No faculty members found matching your search.")
        else:
            print(f"\nFound {len(results)} faculty member(s):")
            print(f"{'ID':<5} {'Name':<25} {'Department':<15} {'Specialization':<20}")
            print("-" * 65)
            
            for faculty in results:
                name = f"{faculty.first_name} {faculty.last_name}"
                print(f"{faculty.id:<5} {name:<25} {faculty.department:<15} {faculty.specialization:<20}")
        
        input("\nPress Enter to continue...")

    def class_management_menu(self):
        """Class management submenu"""
        while True:
            self.display_header("Class Management")
            menu_items = [
                "Add New Class",
                "View All Classes",
                "Search Classes",
                "Update Class Information",
                "Change Class Status",
                "Manage Enrollments",
                "Class Statistics",
                "Export Class Data"
            ]
            
            choice = self.display_menu(menu_items, "Class Management")
            
            if choice == 0:
                break
            elif choice == 1:
                self.add_class()
            elif choice == 2:
                self.view_all_classes()
            elif choice == 3:
                self.search_classes()
            elif choice == 4:
                self.update_class()
            elif choice == 5:
                self.change_class_status()
            elif choice == 6:
                self.manage_enrollments()
            elif choice == 7:
                self.class_statistics()
            elif choice == 8:
                self.export_class_data()

    def add_class(self):
        """Add new class"""
        self.display_header("Add New Class")
        
        print("Enter class information:")
        class_code = input("Class Code: ").strip()
        
        # Show available courses
        courses = self.db.get_all_courses()
        if not courses:
            print("No courses available. Please add courses first.")
            input("Press Enter to continue...")
            return
        
        print("\nAvailable Courses:")
        for course in courses:
            print(f"{course.id}. {course.course_code} - {course.course_name}")
        
        try:
            course_id = int(input("Select Course ID: "))
        except ValueError:
            print("Invalid course ID")
            input("Press Enter to continue...")
            return
        
        # Show available faculty
        faculty_list = self.faculty_manager.get_all_faculty()
        if not faculty_list:
            print("No faculty available. Please add faculty first.")
            input("Press Enter to continue...")
            return
        
        print("\nAvailable Faculty:")
        for faculty in faculty_list:
            print(f"{faculty.id}. {faculty.first_name} {faculty.last_name} - {faculty.department}")
        
        try:
            faculty_id = int(input("Select Faculty ID: "))
        except ValueError:
            print("Invalid faculty ID")
            input("Press Enter to continue...")
            return
        
        semester = input("Semester (e.g., Fall, Spring, Summer): ").strip()
        academic_year = input("Academic Year (e.g., 2024): ").strip()
        schedule = input("Schedule (e.g., MWF 10:00-11:00): ").strip()
        room = input("Room: ").strip()
        
        try:
            max_capacity = int(input("Max Capacity: "))
        except ValueError:
            print("Invalid capacity")
            input("Press Enter to continue...")
            return
        
        result = self.class_manager.add_class(
            class_code, course_id, faculty_id, semester,
            academic_year, schedule, room, max_capacity
        )
        
        print(f"\n{result['message']}")
        input("Press Enter to continue...")

    def view_all_classes(self):
        """View all classes"""
        self.display_header("All Classes")
        
        classes = self.class_manager.get_all_classes()
        
        if not classes:
            print("No classes found.")
        else:
            print(f"{'ID':<5} {'Code':<10} {'Course':<20} {'Faculty':<20} {'Semester':<10} {'Room':<10} {'Enrollment':<10}")
            print("-" * 90)
            
            for class_obj in classes:
                course_name = getattr(class_obj, 'course_name', 'Unknown')
                faculty_name = getattr(class_obj, 'faculty_name', 'Unknown')
                print(f"{class_obj.id:<5} {class_obj.class_code:<10} {course_name:<20} {faculty_name:<20} {class_obj.semester:<10} {class_obj.room:<10} {class_obj.current_enrollment}/{class_obj.max_capacity}")
        
        input("\nPress Enter to continue...")

    def student_management_menu(self):
        """Student management submenu"""
        while True:
            self.display_header("Student Management")
            menu_items = [
                "Add New Student",
                "View All Students",
                "Search Students",
                "Update Student Information",
                "Manage Student Enrollments",
                "Student Statistics",
                "Export Student Data"
            ]
            
            choice = self.display_menu(menu_items, "Student Management")
            
            if choice == 0:
                break
            elif choice == 1:
                self.add_student()
            elif choice == 2:
                self.view_all_students()
            elif choice == 3:
                self.search_students()
            elif choice == 4:
                self.update_student()
            elif choice == 5:
                self.manage_student_enrollments()
            elif choice == 6:
                self.student_statistics()
            elif choice == 7:
                self.export_student_data()

    def add_student(self):
        """Add new student"""
        self.display_header("Add New Student")
        
        print("Enter student information:")
        username = input("Username: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        student_id = input("Student ID: ").strip()
        major = input("Major: ").strip()
        
        try:
            year_level = int(input("Year Level (1-4): "))
            if year_level < 1 or year_level > 4:
                print("Year level must be between 1 and 4")
                input("Press Enter to continue...")
                return
        except ValueError:
            print("Invalid year level")
            input("Press Enter to continue...")
            return
        
        phone = input("Phone: ").strip()
        enrollment_date = datetime.now()
        
        result = self.student_manager.add_student(
            username, email, password, first_name, last_name,
            student_id, major, year_level, phone, enrollment_date
        )
        
        print(f"\n{result['message']}")
        input("Press Enter to continue...")

    def reports_menu(self):
        """Reports and analytics menu"""
        while True:
            self.display_header("Reports & Analytics")
            menu_items = [
                "Faculty Statistics",
                "Class Statistics", 
                "Student Statistics",
                "Enrollment Statistics",
                "Department Statistics",
                "Room Utilization"
            ]
            
            choice = self.display_menu(menu_items, "Reports Menu")
            
            if choice == 0:
                break
            elif choice == 1:
                self.faculty_statistics_report()
            elif choice == 2:
                self.class_statistics_report()
            elif choice == 3:
                self.student_statistics_report()
            elif choice == 4:
                self.enrollment_statistics_report()
            elif choice == 5:
                self.department_statistics_report()
            elif choice == 6:
                self.room_utilization_report()

    def run(self):
        """Main application loop"""
        # Check if admin user exists, if not create one
        if not self.db.authenticate_user("admin", "admin123"):
            print("Creating default admin user...")
            self.db.create_user("admin", "admin@system.com", "admin123", UserRole.ADMIN)
            print("Default admin user created: username=admin, password=admin123")
            input("Press Enter to continue...")
        
        while self.running:
            if not self.auth.is_logged_in():
                if not self.login_menu():
                    break
            else:
                if self.auth.is_admin():
                    self.admin_menu()
                else:
                    print("Only admin access is currently implemented.")
                    input("Press Enter to continue...")
                    self.auth.logout()

if __name__ == "__main__":
    app = FacultyClassManagementSystem()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        input("Press Enter to exit...")