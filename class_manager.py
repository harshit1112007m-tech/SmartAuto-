"""
Class Management System
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from database import DatabaseManager
from models import Class, ClassStatus, Course, Faculty
from auth import AuthenticationManager

class ClassManager:
    def __init__(self, db_manager: DatabaseManager, auth_manager: AuthenticationManager):
        self.db = db_manager
        self.auth = auth_manager

    def add_class(self, class_code: str, course_id: int, faculty_id: int,
                 semester: str, academic_year: str, schedule: str, room: str,
                 max_capacity: int) -> Dict[str, Any]:
        """Add a new class"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"success": False, "message": "Admin permission required"}
        
        try:
            # Validate course exists
            courses = self.db.get_all_courses()
            if not any(c.id == course_id for c in courses):
                return {"success": False, "message": "Course not found"}
            
            # Validate faculty exists
            faculty_list = self.db.get_all_faculty()
            if not any(f.id == faculty_id for f in faculty_list):
                return {"success": False, "message": "Faculty not found"}
            
            class_id = self.db.create_class(
                class_code=class_code,
                course_id=course_id,
                faculty_id=faculty_id,
                semester=semester,
                academic_year=academic_year,
                schedule=schedule,
                room=room,
                max_capacity=max_capacity
            )
            
            return {
                "success": True,
                "message": f"Class {class_code} created successfully",
                "class_id": class_id
            }
        except Exception as e:
            return {"success": False, "message": f"Error creating class: {str(e)}"}

    def get_all_classes(self) -> List[Class]:
        """Get all classes"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return []
        return self.db.get_all_classes()

    def get_class_by_id(self, class_id: int) -> Optional[Class]:
        """Get class by ID"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return None
        return self.db.get_class_by_id(class_id)

    def search_classes(self, search_term: str) -> List[Class]:
        """Search classes by code, course name, or faculty name"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return []
        
        all_classes = self.db.get_all_classes()
        search_term = search_term.lower()
        
        return [
            class_obj for class_obj in all_classes
            if (search_term in class_obj.class_code.lower() or
                search_term in getattr(class_obj, 'course_name', '').lower() or
                search_term in getattr(class_obj, 'faculty_name', '').lower() or
                search_term in class_obj.semester.lower() or
                search_term in class_obj.room.lower())
        ]

    def get_classes_by_semester(self, semester: str, academic_year: str) -> List[Class]:
        """Get classes for specific semester and academic year"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return []
        
        all_classes = self.db.get_all_classes()
        return [
            c for c in all_classes
            if c.semester.lower() == semester.lower() and c.academic_year == academic_year
        ]

    def get_classes_by_faculty(self, faculty_id: int) -> List[Class]:
        """Get all classes taught by a specific faculty member"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return []
        
        all_classes = self.db.get_all_classes()
        return [c for c in all_classes if c.faculty_id == faculty_id]

    def update_class(self, class_id: int, **kwargs) -> Dict[str, Any]:
        """Update class information"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"success": False, "message": "Admin permission required"}
        
        # Remove None values
        update_data = {k: v for k, v in kwargs.items() if v is not None}
        
        if not update_data:
            return {"success": False, "message": "No data to update"}
        
        # Validate faculty if being updated
        if 'faculty_id' in update_data:
            faculty_list = self.db.get_all_faculty()
            if not any(f.id == update_data['faculty_id'] for f in faculty_list):
                return {"success": False, "message": "Faculty not found"}
        
        # Validate course if being updated
        if 'course_id' in update_data:
            courses = self.db.get_all_courses()
            if not any(c.id == update_data['course_id'] for c in courses):
                return {"success": False, "message": "Course not found"}
        
        success = self.db.update_class(class_id, **update_data)
        
        if success:
            return {"success": True, "message": "Class information updated successfully"}
        else:
            return {"success": False, "message": "Class not found or update failed"}

    def change_class_status(self, class_id: int, status: ClassStatus) -> Dict[str, Any]:
        """Change class status (active/inactive/completed)"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"success": False, "message": "Admin permission required"}
        
        success = self.db.update_class(class_id, status=status.value)
        
        if success:
            return {"success": True, "message": f"Class status changed to {status.value}"}
        else:
            return {"success": False, "message": "Class not found or status change failed"}

    def get_class_enrollments(self, class_id: int) -> List[Dict[str, Any]]:
        """Get all enrollments for a class"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return []
        
        return self.db.get_class_enrollments(class_id)

    def enroll_student(self, student_id: int, class_id: int) -> Dict[str, Any]:
        """Enroll student in a class"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"success": False, "message": "Admin permission required"}
        
        success = self.db.enroll_student(student_id, class_id)
        
        if success:
            return {"success": True, "message": "Student enrolled successfully"}
        else:
            return {"success": False, "message": "Enrollment failed - class may be full or student already enrolled"}

    def drop_student(self, student_id: int, class_id: int) -> Dict[str, Any]:
        """Drop student from a class"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"success": False, "message": "Admin permission required"}
        
        success = self.db.drop_student(student_id, class_id)
        
        if success:
            return {"success": True, "message": "Student dropped successfully"}
        else:
            return {"success": False, "message": "Drop failed - student not enrolled in this class"}

    def get_class_statistics(self) -> Dict[str, Any]:
        """Get overall class statistics"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {}
        
        all_classes = self.db.get_all_classes()
        
        total_classes = len(all_classes)
        active_classes = len([c for c in all_classes if c.status == ClassStatus.ACTIVE])
        total_enrollment = sum(c.current_enrollment for c in all_classes)
        total_capacity = sum(c.max_capacity for c in all_classes)
        
        # Calculate average class size
        avg_class_size = total_enrollment / total_classes if total_classes > 0 else 0
        
        # Calculate capacity utilization
        capacity_utilization = (total_enrollment / total_capacity * 100) if total_capacity > 0 else 0
        
        # Get semester breakdown
        semester_stats = {}
        for class_obj in all_classes:
            key = f"{class_obj.academic_year} {class_obj.semester}"
            if key not in semester_stats:
                semester_stats[key] = {"classes": 0, "enrollment": 0, "capacity": 0}
            semester_stats[key]["classes"] += 1
            semester_stats[key]["enrollment"] += class_obj.current_enrollment
            semester_stats[key]["capacity"] += class_obj.max_capacity
        
        return {
            "total_classes": total_classes,
            "active_classes": active_classes,
            "total_enrollment": total_enrollment,
            "total_capacity": total_capacity,
            "average_class_size": round(avg_class_size, 2),
            "capacity_utilization": round(capacity_utilization, 2),
            "semester_breakdown": semester_stats
        }

    def get_room_utilization(self) -> Dict[str, Any]:
        """Get room utilization statistics"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {}
        
        all_classes = self.db.get_all_classes()
        room_stats = {}
        
        for class_obj in all_classes:
            room = class_obj.room
            if room not in room_stats:
                room_stats[room] = {
                    "total_classes": 0,
                    "total_hours": 0,
                    "utilization_rate": 0
                }
            room_stats[room]["total_classes"] += 1
            # Simple calculation - assume each class is 3 hours per week
            room_stats[room]["total_hours"] += 3
        
        # Calculate utilization rate (assuming 40 hours per week capacity)
        for room, stats in room_stats.items():
            stats["utilization_rate"] = round((stats["total_hours"] / 40) * 100, 2)
        
        return room_stats

    def get_faculty_workload_summary(self) -> List[Dict[str, Any]]:
        """Get workload summary for all faculty"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return []
        
        faculty_list = self.db.get_all_faculty()
        workload_summary = []
        
        for faculty in faculty_list:
            workload = self.db.get_faculty_workload(faculty.id)
            workload_summary.append({
                "faculty_id": faculty.id,
                "name": f"{faculty.first_name} {faculty.last_name}",
                "department": faculty.department,
                "total_classes": workload["total_classes"],
                "total_students": workload["total_students"],
                "avg_class_size": workload["avg_class_size"]
            })
        
        return sorted(workload_summary, key=lambda x: x["total_students"], reverse=True)

    def export_class_data(self, filename: str = None) -> Dict[str, Any]:
        """Export class data to CSV format"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"success": False, "message": "Admin permission required"}
        
        if not filename:
            filename = f"class_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            all_classes = self.db.get_all_classes()
            
            # Create CSV content
            csv_content = "Class ID,Class Code,Course Name,Faculty Name,Semester,Academic Year,Schedule,Room,Enrollment,Capacity,Status\n"
            
            for class_obj in all_classes:
                csv_content += f"{class_obj.id},{class_obj.class_code},"
                csv_content += f"{getattr(class_obj, 'course_name', 'Unknown')},"
                csv_content += f"{getattr(class_obj, 'faculty_name', 'Unknown')},"
                csv_content += f"{class_obj.semester},{class_obj.academic_year},"
                csv_content += f"{class_obj.schedule},{class_obj.room},"
                csv_content += f"{class_obj.current_enrollment},{class_obj.max_capacity},"
                csv_content += f"{class_obj.status.value}\n"
            
            # Write to file
            with open(filename, 'w') as f:
                f.write(csv_content)
            
            return {
                "success": True,
                "message": f"Class data exported to {filename}",
                "filename": filename,
                "records_exported": len(all_classes)
            }
        except Exception as e:
            return {"success": False, "message": f"Export failed: {str(e)}"}

    def validate_class_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate class data before creation/update"""
        errors = []
        
        required_fields = ['class_code', 'course_id', 'faculty_id', 'semester', 
                          'academic_year', 'schedule', 'room', 'max_capacity']
        
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"{field.replace('_', ' ').title()} is required")
        
        # Validate max_capacity
        if 'max_capacity' in data:
            try:
                capacity = int(data['max_capacity'])
                if capacity <= 0:
                    errors.append("Max capacity must be positive")
            except (ValueError, TypeError):
                errors.append("Max capacity must be a valid integer")
        
        # Validate academic year format
        if 'academic_year' in data and data['academic_year']:
            year = str(data['academic_year'])
            if not year.isdigit() or len(year) != 4:
                errors.append("Academic year must be a 4-digit year")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }