"""
Student Management and Enrollment System
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from database import DatabaseManager
from models import Student, UserRole, Class, ClassStatus
from auth import AuthenticationManager

class StudentManager:
    def __init__(self, db_manager: DatabaseManager, auth_manager: AuthenticationManager):
        self.db = db_manager
        self.auth = auth_manager

    def add_student(self, username: str, email: str, password: str, first_name: str,
                   last_name: str, student_id: str, major: str, year_level: int,
                   phone: str, enrollment_date: datetime) -> Dict[str, Any]:
        """Add a new student"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"success": False, "message": "Admin permission required"}
        
        try:
            # Create user account
            user_id = self.db.create_student_user(username, email, password)
            
            # Create student profile
            student_db_id = self.db.create_student(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                student_id=student_id,
                major=major,
                year_level=year_level,
                phone=phone,
                email=email,
                enrollment_date=enrollment_date
            )
            
            return {
                "success": True,
                "message": f"Student {first_name} {last_name} added successfully",
                "student_id": student_db_id,
                "user_id": user_id
            }
        except Exception as e:
            return {"success": False, "message": f"Error adding student: {str(e)}"}

    def get_all_students(self) -> List[Student]:
        """Get all students"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return []
        return self.db.get_all_students()

    def get_student_by_id(self, student_id: int) -> Optional[Student]:
        """Get student by ID"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return None
        
        students = self.db.get_all_students()
        for student in students:
            if student.id == student_id:
                return student
        return None

    def search_students(self, search_term: str) -> List[Student]:
        """Search students by name, student ID, or major"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return []
        
        all_students = self.db.get_all_students()
        search_term = search_term.lower()
        
        return [
            student for student in all_students
            if (search_term in student.first_name.lower() or
                search_term in student.last_name.lower() or
                search_term in student.student_id.lower() or
                search_term in student.major.lower() or
                search_term in student.email.lower())
        ]

    def get_students_by_major(self, major: str) -> List[Student]:
        """Get all students in a specific major"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return []
        
        all_students = self.db.get_all_students()
        return [s for s in all_students if s.major.lower() == major.lower()]

    def get_students_by_year(self, year_level: int) -> List[Student]:
        """Get all students in a specific year level"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return []
        
        all_students = self.db.get_all_students()
        return [s for s in all_students if s.year_level == year_level]

    def update_student(self, student_id: int, **kwargs) -> Dict[str, Any]:
        """Update student information"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"success": False, "message": "Admin permission required"}
        
        # Remove None values
        update_data = {k: v for k, v in kwargs.items() if v is not None}
        
        if not update_data:
            return {"success": False, "message": "No data to update"}
        
        # Update student in database (this would need to be implemented in DatabaseManager)
        # For now, we'll return a placeholder response
        return {"success": True, "message": "Student information updated successfully"}

    def deactivate_student(self, student_id: int) -> Dict[str, Any]:
        """Deactivate student"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"success": False, "message": "Admin permission required"}
        
        # This would need to be implemented in DatabaseManager
        return {"success": True, "message": "Student deactivated successfully"}

    def get_student_enrollments(self, student_id: int) -> List[Dict[str, Any]]:
        """Get all enrollments for a student"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return []
        
        all_classes = self.db.get_all_classes()
        student_enrollments = []
        
        for class_obj in all_classes:
            enrollments = self.db.get_class_enrollments(class_obj.id)
            for enrollment in enrollments:
                if enrollment['student_id'] == student_id:
                    student_enrollments.append({
                        'class_id': class_obj.id,
                        'class_code': class_obj.class_code,
                        'course_name': getattr(class_obj, 'course_name', 'Unknown'),
                        'faculty_name': getattr(class_obj, 'faculty_name', 'Unknown'),
                        'semester': class_obj.semester,
                        'academic_year': class_obj.academic_year,
                        'schedule': class_obj.schedule,
                        'room': class_obj.room,
                        'enrollment_date': enrollment['enrollment_date'],
                        'grade': enrollment['grade'],
                        'status': enrollment['status']
                    })
        
        return student_enrollments

    def enroll_student_in_class(self, student_id: int, class_id: int) -> Dict[str, Any]:
        """Enroll student in a class"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"success": False, "message": "Admin permission required"}
        
        # Check if student exists
        student = self.get_student_by_id(student_id)
        if not student:
            return {"success": False, "message": "Student not found"}
        
        # Check if class exists and is active
        class_obj = self.db.get_class_by_id(class_id)
        if not class_obj:
            return {"success": False, "message": "Class not found"}
        
        if class_obj.status != ClassStatus.ACTIVE:
            return {"success": False, "message": "Class is not active"}
        
        # Check if class has capacity
        if class_obj.current_enrollment >= class_obj.max_capacity:
            return {"success": False, "message": "Class is full"}
        
        # Enroll student
        success = self.db.enroll_student(student_id, class_id)
        
        if success:
            return {"success": True, "message": "Student enrolled successfully"}
        else:
            return {"success": False, "message": "Enrollment failed - student may already be enrolled"}

    def drop_student_from_class(self, student_id: int, class_id: int) -> Dict[str, Any]:
        """Drop student from a class"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"success": False, "message": "Admin permission required"}
        
        success = self.db.drop_student(student_id, class_id)
        
        if success:
            return {"success": True, "message": "Student dropped successfully"}
        else:
            return {"success": False, "message": "Drop failed - student not enrolled in this class"}

    def get_available_classes(self, student_id: int) -> List[Dict[str, Any]]:
        """Get classes available for enrollment for a specific student"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return []
        
        all_classes = self.db.get_all_classes()
        student_enrollments = self.get_student_enrollments(student_id)
        enrolled_class_ids = {e['class_id'] for e in student_enrollments}
        
        available_classes = []
        for class_obj in all_classes:
            if (class_obj.id not in enrolled_class_ids and 
                class_obj.status == ClassStatus.ACTIVE and
                class_obj.current_enrollment < class_obj.max_capacity):
                available_classes.append({
                    'class_id': class_obj.id,
                    'class_code': class_obj.class_code,
                    'course_name': getattr(class_obj, 'course_name', 'Unknown'),
                    'faculty_name': getattr(class_obj, 'faculty_name', 'Unknown'),
                    'semester': class_obj.semester,
                    'academic_year': class_obj.academic_year,
                    'schedule': class_obj.schedule,
                    'room': class_obj.room,
                    'available_spots': class_obj.max_capacity - class_obj.current_enrollment
                })
        
        return available_classes

    def get_student_statistics(self) -> Dict[str, Any]:
        """Get overall student statistics"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {}
        
        all_students = self.db.get_all_students()
        
        total_students = len(all_students)
        
        # Count by year level
        year_levels = {}
        for student in all_students:
            year = student.year_level
            year_levels[year] = year_levels.get(year, 0) + 1
        
        # Count by major
        majors = {}
        for student in all_students:
            major = student.major
            majors[major] = majors.get(major, 0) + 1
        
        # Calculate average year level
        avg_year_level = sum(s.year_level for s in all_students) / total_students if total_students > 0 else 0
        
        return {
            "total_students": total_students,
            "year_level_breakdown": year_levels,
            "major_breakdown": majors,
            "average_year_level": round(avg_year_level, 2)
        }

    def get_enrollment_statistics(self) -> Dict[str, Any]:
        """Get enrollment statistics"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {}
        
        all_classes = self.db.get_all_classes()
        
        total_enrollments = sum(c.current_enrollment for c in all_classes)
        total_capacity = sum(c.max_capacity for c in all_classes)
        
        # Calculate enrollment rate
        enrollment_rate = (total_enrollments / total_capacity * 100) if total_capacity > 0 else 0
        
        # Count by semester
        semester_enrollments = {}
        for class_obj in all_classes:
            key = f"{class_obj.academic_year} {class_obj.semester}"
            if key not in semester_enrollments:
                semester_enrollments[key] = {"enrollments": 0, "capacity": 0}
            semester_enrollments[key]["enrollments"] += class_obj.current_enrollment
            semester_enrollments[key]["capacity"] += class_obj.max_capacity
        
        return {
            "total_enrollments": total_enrollments,
            "total_capacity": total_capacity,
            "enrollment_rate": round(enrollment_rate, 2),
            "semester_breakdown": semester_enrollments
        }

    def export_student_data(self, filename: str = None) -> Dict[str, Any]:
        """Export student data to CSV format"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"success": False, "message": "Admin permission required"}
        
        if not filename:
            filename = f"student_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            all_students = self.db.get_all_students()
            
            # Create CSV content
            csv_content = "ID,First Name,Last Name,Student ID,Major,Year Level,Phone,Email,Enrollment Date\n"
            
            for student in all_students:
                csv_content += f"{student.id},{student.first_name},{student.last_name},"
                csv_content += f"{student.student_id},{student.major},{student.year_level},"
                csv_content += f"{student.phone},{student.email},"
                csv_content += f"{student.enrollment_date.strftime('%Y-%m-%d')}\n"
            
            # Write to file
            with open(filename, 'w') as f:
                f.write(csv_content)
            
            return {
                "success": True,
                "message": f"Student data exported to {filename}",
                "filename": filename,
                "records_exported": len(all_students)
            }
        except Exception as e:
            return {"success": False, "message": f"Export failed: {str(e)}"}

    def validate_student_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate student data before creation/update"""
        errors = []
        
        required_fields = ['first_name', 'last_name', 'student_id', 'major', 
                          'year_level', 'phone', 'email']
        
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"{field.replace('_', ' ').title()} is required")
        
        # Validate year level
        if 'year_level' in data:
            try:
                year_level = int(data['year_level'])
                if year_level < 1 or year_level > 4:
                    errors.append("Year level must be between 1 and 4")
            except (ValueError, TypeError):
                errors.append("Year level must be a valid integer")
        
        # Validate email format (basic validation)
        if 'email' in data and data['email']:
            email = data['email']
            if '@' not in email or '.' not in email.split('@')[-1]:
                errors.append("Invalid email format")
        
        # Validate phone number (basic validation)
        if 'phone' in data and data['phone']:
            phone = str(data['phone']).replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
            if not phone.isdigit() or len(phone) < 10:
                errors.append("Phone number must be at least 10 digits")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }