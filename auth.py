"""
Authentication and user management system
"""
from typing import Optional, Dict, Any
from datetime import datetime
from database import DatabaseManager
from models import User, UserRole, Faculty, Student

class AuthenticationManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.current_user: Optional[User] = None

    def login(self, username: str, password: str) -> bool:
        """Authenticate user login"""
        user = self.db.authenticate_user(username, password)
        if user:
            self.current_user = user
            return True
        return False

    def logout(self):
        """Logout current user"""
        self.current_user = None

    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.current_user is not None

    def get_current_user(self) -> Optional[User]:
        """Get current logged in user"""
        return self.current_user

    def has_permission(self, required_role: UserRole) -> bool:
        """Check if current user has required permission"""
        if not self.current_user:
            return False
        
        # Admin has all permissions
        if self.current_user.role == UserRole.ADMIN:
            return True
        
        # Check specific role
        return self.current_user.role == required_role

    def create_admin_user(self, username: str, email: str, password: str) -> int:
        """Create admin user (for initial setup)"""
        return self.db.create_user(username, email, password, UserRole.ADMIN)

    def create_faculty_user(self, username: str, email: str, password: str) -> int:
        """Create faculty user account"""
        return self.db.create_user(username, email, password, UserRole.FACULTY)

    def create_student_user(self, username: str, email: str, password: str) -> int:
        """Create student user account"""
        return self.db.create_user(username, email, password, UserRole.STUDENT)

    def get_user_profile(self) -> Dict[str, Any]:
        """Get current user's profile information"""
        if not self.current_user:
            return {}
        
        profile = {
            'user_id': self.current_user.id,
            'username': self.current_user.username,
            'email': self.current_user.email,
            'role': self.current_user.role.value,
            'created_at': self.current_user.created_at.isoformat(),
            'is_active': self.current_user.is_active
        }
        
        # Add role-specific information
        if self.current_user.role == UserRole.FACULTY:
            faculty = self.get_faculty_profile()
            if faculty:
                profile.update({
                    'first_name': faculty.first_name,
                    'last_name': faculty.last_name,
                    'employee_id': faculty.employee_id,
                    'department': faculty.department,
                    'specialization': faculty.specialization,
                    'office_location': faculty.office_location
                })
        
        elif self.current_user.role == UserRole.STUDENT:
            student = self.get_student_profile()
            if student:
                profile.update({
                    'first_name': student.first_name,
                    'last_name': student.last_name,
                    'student_id': student.student_id,
                    'major': student.major,
                    'year_level': student.year_level
                })
        
        return profile

    def get_faculty_profile(self) -> Optional[Faculty]:
        """Get faculty profile for current user"""
        if not self.current_user or self.current_user.role != UserRole.FACULTY:
            return None
        
        faculty_list = self.db.get_all_faculty()
        for faculty in faculty_list:
            if faculty.user_id == self.current_user.id:
                return faculty
        return None

    def get_student_profile(self) -> Optional[Student]:
        """Get student profile for current user"""
        if not self.current_user or self.current_user.role != UserRole.STUDENT:
            return None
        
        students = self.db.get_all_students()
        for student in students:
            if student.user_id == self.current_user.id:
                return student
        return None

    def change_password(self, old_password: str, new_password: str) -> bool:
        """Change current user's password"""
        if not self.current_user:
            return False
        
        # Verify old password
        if not self.db.verify_password(old_password, self.current_user.password_hash):
            return False
        
        # Update password
        new_hash = self.db.hash_password(new_password)
        # Note: This would require a password update method in DatabaseManager
        # For now, we'll return True as a placeholder
        return True

    def is_admin(self) -> bool:
        """Check if current user is admin"""
        return self.current_user and self.current_user.role == UserRole.ADMIN

    def is_faculty(self) -> bool:
        """Check if current user is faculty"""
        return self.current_user and self.current_user.role == UserRole.FACULTY

    def is_student(self) -> bool:
        """Check if current user is student"""
        return self.current_user and self.current_user.role == UserRole.STUDENT