"""
Faculty Management System
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from database import DatabaseManager
from models import Faculty, UserRole
from auth import AuthenticationManager

class FacultyManager:
    def __init__(self, db_manager: DatabaseManager, auth_manager: AuthenticationManager):
        self.db = db_manager
        self.auth = auth_manager

    def add_faculty(self, username: str, email: str, password: str, first_name: str,
                   last_name: str, employee_id: str, department: str, specialization: str,
                   phone: str, office_location: str, hire_date: datetime, salary: float) -> Dict[str, Any]:
        """Add a new faculty member"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"success": False, "message": "Admin permission required"}
        
        try:
            # Create user account
            user_id = self.db.create_faculty_user(username, email, password)
            
            # Create faculty profile
            faculty_id = self.db.create_faculty(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                employee_id=employee_id,
                department=department,
                specialization=specialization,
                phone=phone,
                office_location=office_location,
                hire_date=hire_date,
                salary=salary
            )
            
            return {
                "success": True,
                "message": f"Faculty member {first_name} {last_name} added successfully",
                "faculty_id": faculty_id,
                "user_id": user_id
            }
        except Exception as e:
            return {"success": False, "message": f"Error adding faculty: {str(e)}"}

    def get_all_faculty(self) -> List[Faculty]:
        """Get all faculty members"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return []
        return self.db.get_all_faculty()

    def get_faculty_by_id(self, faculty_id: int) -> Optional[Faculty]:
        """Get faculty by ID"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return None
        return self.db.get_faculty_by_id(faculty_id)

    def search_faculty(self, search_term: str) -> List[Faculty]:
        """Search faculty by name, department, or specialization"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return []
        
        all_faculty = self.db.get_all_faculty()
        search_term = search_term.lower()
        
        return [
            faculty for faculty in all_faculty
            if (search_term in faculty.first_name.lower() or
                search_term in faculty.last_name.lower() or
                search_term in faculty.department.lower() or
                search_term in faculty.specialization.lower() or
                search_term in faculty.employee_id.lower())
        ]

    def update_faculty(self, faculty_id: int, **kwargs) -> Dict[str, Any]:
        """Update faculty information"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"success": False, "message": "Admin permission required"}
        
        # Remove None values
        update_data = {k: v for k, v in kwargs.items() if v is not None}
        
        if not update_data:
            return {"success": False, "message": "No data to update"}
        
        success = self.db.update_faculty(faculty_id, **update_data)
        
        if success:
            return {"success": True, "message": "Faculty information updated successfully"}
        else:
            return {"success": False, "message": "Faculty not found or update failed"}

    def deactivate_faculty(self, faculty_id: int) -> Dict[str, Any]:
        """Deactivate faculty member"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"success": False, "message": "Admin permission required"}
        
        success = self.db.deactivate_faculty(faculty_id)
        
        if success:
            return {"success": True, "message": "Faculty member deactivated successfully"}
        else:
            return {"success": False, "message": "Faculty not found or deactivation failed"}

    def get_faculty_workload(self, faculty_id: int) -> Dict[str, Any]:
        """Get faculty workload statistics"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {}
        
        workload = self.db.get_faculty_workload(faculty_id)
        faculty = self.db.get_faculty_by_id(faculty_id)
        
        if not faculty:
            return {"error": "Faculty not found"}
        
        return {
            "faculty_name": f"{faculty.first_name} {faculty.last_name}",
            "employee_id": faculty.employee_id,
            "department": faculty.department,
            "workload": workload
        }

    def get_department_faculty(self, department: str) -> List[Faculty]:
        """Get all faculty in a specific department"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return []
        
        all_faculty = self.db.get_all_faculty()
        return [f for f in all_faculty if f.department.lower() == department.lower()]

    def get_faculty_classes(self, faculty_id: int) -> List[Dict[str, Any]]:
        """Get all classes taught by a faculty member"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return []
        
        all_classes = self.db.get_all_classes()
        faculty_classes = [c for c in all_classes if c.faculty_id == faculty_id]
        
        return [
            {
                "class_id": c.id,
                "class_code": c.class_code,
                "course_name": getattr(c, 'course_name', 'Unknown'),
                "semester": c.semester,
                "academic_year": c.academic_year,
                "schedule": c.schedule,
                "room": c.room,
                "enrollment": c.current_enrollment,
                "max_capacity": c.max_capacity,
                "status": c.status.value
            }
            for c in faculty_classes
        ]

    def get_faculty_statistics(self) -> Dict[str, Any]:
        """Get overall faculty statistics"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {}
        
        faculty_list = self.db.get_all_faculty()
        dept_stats = self.db.get_department_statistics()
        
        total_faculty = len(faculty_list)
        departments = len(set(f.department for f in faculty_list))
        
        # Calculate average salary
        total_salary = sum(f.salary for f in faculty_list)
        avg_salary = total_salary / total_faculty if total_faculty > 0 else 0
        
        return {
            "total_faculty": total_faculty,
            "total_departments": departments,
            "average_salary": round(avg_salary, 2),
            "department_breakdown": dept_stats
        }

    def export_faculty_data(self, filename: str = None) -> Dict[str, Any]:
        """Export faculty data to CSV format"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"success": False, "message": "Admin permission required"}
        
        if not filename:
            filename = f"faculty_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            faculty_list = self.db.get_all_faculty()
            
            # Create CSV content
            csv_content = "ID,First Name,Last Name,Employee ID,Department,Specialization,Phone,Office,Salary,Hire Date\n"
            
            for faculty in faculty_list:
                csv_content += f"{faculty.id},{faculty.first_name},{faculty.last_name},"
                csv_content += f"{faculty.employee_id},{faculty.department},{faculty.specialization},"
                csv_content += f"{faculty.phone},{faculty.office_location},{faculty.salary},"
                csv_content += f"{faculty.hire_date.strftime('%Y-%m-%d')}\n"
            
            # Write to file
            with open(filename, 'w') as f:
                f.write(csv_content)
            
            return {
                "success": True,
                "message": f"Faculty data exported to {filename}",
                "filename": filename,
                "records_exported": len(faculty_list)
            }
        except Exception as e:
            return {"success": False, "message": f"Export failed: {str(e)}"}

    def validate_faculty_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate faculty data before creation/update"""
        errors = []
        
        required_fields = ['first_name', 'last_name', 'employee_id', 'department', 
                          'specialization', 'phone', 'office_location', 'salary']
        
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"{field.replace('_', ' ').title()} is required")
        
        # Validate salary
        if 'salary' in data:
            try:
                salary = float(data['salary'])
                if salary < 0:
                    errors.append("Salary must be positive")
            except (ValueError, TypeError):
                errors.append("Salary must be a valid number")
        
        # Validate phone number (basic validation)
        if 'phone' in data and data['phone']:
            phone = str(data['phone']).replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
            if not phone.isdigit() or len(phone) < 10:
                errors.append("Phone number must be at least 10 digits")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }