"""
Reporting and Analytics System
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from database import DatabaseManager
from auth import AuthenticationManager
from models import UserRole

class ReportGenerator:
    def __init__(self, db_manager: DatabaseManager, auth_manager: AuthenticationManager):
        self.db = db_manager
        self.auth = auth_manager

    def generate_faculty_report(self) -> Dict[str, Any]:
        """Generate comprehensive faculty report"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"error": "Admin permission required"}
        
        faculty_list = self.db.get_all_faculty()
        dept_stats = self.db.get_department_statistics()
        
        # Calculate statistics
        total_faculty = len(faculty_list)
        departments = len(set(f.department for f in faculty_list))
        avg_salary = sum(f.salary for f in faculty_list) / total_faculty if total_faculty > 0 else 0
        
        # Faculty by department
        dept_breakdown = {}
        for faculty in faculty_list:
            dept = faculty.department
            if dept not in dept_breakdown:
                dept_breakdown[dept] = {
                    "count": 0,
                    "total_salary": 0,
                    "avg_salary": 0,
                    "faculty": []
                }
            dept_breakdown[dept]["count"] += 1
            dept_breakdown[dept]["total_salary"] += faculty.salary
            dept_breakdown[dept]["faculty"].append(faculty)
        
        # Calculate average salary per department
        for dept in dept_breakdown:
            dept_breakdown[dept]["avg_salary"] = dept_breakdown[dept]["total_salary"] / dept_breakdown[dept]["count"]
        
        return {
            "report_type": "Faculty Report",
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_faculty": total_faculty,
                "total_departments": departments,
                "average_salary": round(avg_salary, 2)
            },
            "department_breakdown": dept_breakdown,
            "detailed_stats": dept_stats
        }

    def generate_class_report(self) -> Dict[str, Any]:
        """Generate comprehensive class report"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"error": "Admin permission required"}
        
        all_classes = self.db.get_all_classes()
        
        # Basic statistics
        total_classes = len(all_classes)
        active_classes = len([c for c in all_classes if c.status.value == "active"])
        total_enrollment = sum(c.current_enrollment for c in all_classes)
        total_capacity = sum(c.max_capacity for c in all_classes)
        
        # Semester breakdown
        semester_stats = {}
        for class_obj in all_classes:
            key = f"{class_obj.academic_year} {class_obj.semester}"
            if key not in semester_stats:
                semester_stats[key] = {
                    "classes": 0,
                    "enrollment": 0,
                    "capacity": 0,
                    "utilization": 0
                }
            semester_stats[key]["classes"] += 1
            semester_stats[key]["enrollment"] += class_obj.current_enrollment
            semester_stats[key]["capacity"] += class_obj.max_capacity
        
        # Calculate utilization rates
        for key in semester_stats:
            stats = semester_stats[key]
            if stats["capacity"] > 0:
                stats["utilization"] = round((stats["enrollment"] / stats["capacity"]) * 100, 2)
        
        # Room utilization
        room_stats = {}
        for class_obj in all_classes:
            room = class_obj.room
            if room not in room_stats:
                room_stats[room] = {
                    "classes": 0,
                    "total_hours": 0,
                    "utilization_rate": 0
                }
            room_stats[room]["classes"] += 1
            room_stats[room]["total_hours"] += 3  # Assume 3 hours per class per week
        
        # Calculate room utilization (assuming 40 hours per week capacity)
        for room in room_stats:
            room_stats[room]["utilization_rate"] = round((room_stats[room]["total_hours"] / 40) * 100, 2)
        
        return {
            "report_type": "Class Report",
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_classes": total_classes,
                "active_classes": active_classes,
                "total_enrollment": total_enrollment,
                "total_capacity": total_capacity,
                "overall_utilization": round((total_enrollment / total_capacity * 100), 2) if total_capacity > 0 else 0
            },
            "semester_breakdown": semester_stats,
            "room_utilization": room_stats
        }

    def generate_enrollment_report(self) -> Dict[str, Any]:
        """Generate enrollment analysis report"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"error": "Admin permission required"}
        
        all_classes = self.db.get_all_classes()
        all_students = self.db.get_all_students()
        
        # Enrollment trends by semester
        semester_enrollments = {}
        for class_obj in all_classes:
            key = f"{class_obj.academic_year} {class_obj.semester}"
            if key not in semester_enrollments:
                semester_enrollments[key] = {
                    "classes": 0,
                    "enrollment": 0,
                    "capacity": 0,
                    "avg_class_size": 0
                }
            semester_enrollments[key]["classes"] += 1
            semester_enrollments[key]["enrollment"] += class_obj.current_enrollment
            semester_enrollments[key]["capacity"] += class_obj.max_capacity
        
        # Calculate average class size per semester
        for key in semester_enrollments:
            stats = semester_enrollments[key]
            if stats["classes"] > 0:
                stats["avg_class_size"] = round(stats["enrollment"] / stats["classes"], 2)
        
        # Student enrollment distribution
        student_enrollment_counts = {}
        for student in all_students:
            # Count enrollments for each student
            enrollments = self.student_manager.get_student_enrollments(student.id)
            count = len(enrollments)
            if count not in student_enrollment_counts:
                student_enrollment_counts[count] = 0
            student_enrollment_counts[count] += 1
        
        return {
            "report_type": "Enrollment Report",
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_students": len(all_students),
                "total_classes": len(all_classes),
                "total_enrollments": sum(c.current_enrollment for c in all_classes)
            },
            "semester_trends": semester_enrollments,
            "student_enrollment_distribution": student_enrollment_counts
        }

    def generate_department_report(self) -> Dict[str, Any]:
        """Generate department performance report"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"error": "Admin permission required"}
        
        dept_stats = self.db.get_department_statistics()
        faculty_list = self.db.get_all_faculty()
        all_classes = self.db.get_all_classes()
        
        # Enhanced department statistics
        enhanced_stats = {}
        for dept in dept_stats:
            dept_name = dept["department"]
            enhanced_stats[dept_name] = {
                "faculty_count": dept["faculty_count"],
                "class_count": dept["class_count"],
                "total_enrollment": dept["total_enrollment"],
                "avg_class_size": 0,
                "faculty_workload": 0
            }
            
            # Calculate average class size
            if dept["class_count"] > 0:
                enhanced_stats[dept_name]["avg_class_size"] = round(
                    dept["total_enrollment"] / dept["class_count"], 2
                )
            
            # Calculate average faculty workload
            if dept["faculty_count"] > 0:
                enhanced_stats[dept_name]["faculty_workload"] = round(
                    dept["class_count"] / dept["faculty_count"], 2
                )
        
        return {
            "report_type": "Department Report",
            "generated_at": datetime.now().isoformat(),
            "department_statistics": enhanced_stats
        }

    def generate_faculty_workload_report(self) -> Dict[str, Any]:
        """Generate faculty workload analysis"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"error": "Admin permission required"}
        
        faculty_list = self.db.get_all_faculty()
        workload_data = []
        
        for faculty in faculty_list:
            workload = self.db.get_faculty_workload(faculty.id)
            workload_data.append({
                "faculty_id": faculty.id,
                "name": f"{faculty.first_name} {faculty.last_name}",
                "department": faculty.department,
                "employee_id": faculty.employee_id,
                "total_classes": workload["total_classes"],
                "total_students": workload["total_students"],
                "avg_class_size": workload["avg_class_size"]
            })
        
        # Sort by total students (workload)
        workload_data.sort(key=lambda x: x["total_students"], reverse=True)
        
        # Calculate statistics
        total_faculty = len(workload_data)
        avg_classes = sum(w["total_classes"] for w in workload_data) / total_faculty if total_faculty > 0 else 0
        avg_students = sum(w["total_students"] for w in workload_data) / total_faculty if total_faculty > 0 else 0
        
        return {
            "report_type": "Faculty Workload Report",
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_faculty": total_faculty,
                "average_classes_per_faculty": round(avg_classes, 2),
                "average_students_per_faculty": round(avg_students, 2)
            },
            "faculty_workloads": workload_data
        }

    def generate_room_utilization_report(self) -> Dict[str, Any]:
        """Generate room utilization analysis"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"error": "Admin permission required"}
        
        all_classes = self.db.get_all_classes()
        room_stats = {}
        
        for class_obj in all_classes:
            room = class_obj.room
            if room not in room_stats:
                room_stats[room] = {
                    "classes": 0,
                    "total_hours": 0,
                    "utilization_rate": 0,
                    "class_details": []
                }
            
            room_stats[room]["classes"] += 1
            room_stats[room]["total_hours"] += 3  # Assume 3 hours per class per week
            room_stats[room]["class_details"].append({
                "class_code": class_obj.class_code,
                "course_name": getattr(class_obj, 'course_name', 'Unknown'),
                "schedule": class_obj.schedule,
                "enrollment": class_obj.current_enrollment
            })
        
        # Calculate utilization rates
        for room in room_stats:
            room_stats[room]["utilization_rate"] = round((room_stats[room]["total_hours"] / 40) * 100, 2)
        
        # Sort by utilization rate
        sorted_rooms = sorted(room_stats.items(), key=lambda x: x[1]["utilization_rate"], reverse=True)
        
        return {
            "report_type": "Room Utilization Report",
            "generated_at": datetime.now().isoformat(),
            "room_utilization": dict(sorted_rooms)
        }

    def export_report_to_csv(self, report_data: Dict[str, Any], filename: str = None) -> Dict[str, Any]:
        """Export report data to CSV format"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"success": False, "message": "Admin permission required"}
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_type = report_data.get("report_type", "report").replace(" ", "_").lower()
            filename = f"{report_type}_{timestamp}.csv"
        
        try:
            with open(filename, 'w') as f:
                # Write header
                f.write(f"Report: {report_data.get('report_type', 'Unknown')}\n")
                f.write(f"Generated: {report_data.get('generated_at', 'Unknown')}\n\n")
                
                # Write summary data
                if "summary" in report_data:
                    f.write("SUMMARY\n")
                    f.write("-------\n")
                    for key, value in report_data["summary"].items():
                        f.write(f"{key.replace('_', ' ').title()}: {value}\n")
                    f.write("\n")
                
                # Write detailed data based on report type
                if "faculty_workloads" in report_data:
                    f.write("FACULTY WORKLOAD DETAILS\n")
                    f.write("ID,Name,Department,Employee ID,Classes,Students,Avg Class Size\n")
                    for faculty in report_data["faculty_workloads"]:
                        f.write(f"{faculty['faculty_id']},{faculty['name']},{faculty['department']},")
                        f.write(f"{faculty['employee_id']},{faculty['total_classes']},{faculty['total_students']},")
                        f.write(f"{faculty['avg_class_size']}\n")
                
                elif "room_utilization" in report_data:
                    f.write("ROOM UTILIZATION DETAILS\n")
                    f.write("Room,Classes,Total Hours,Utilization Rate\n")
                    for room, stats in report_data["room_utilization"].items():
                        f.write(f"{room},{stats['classes']},{stats['total_hours']},{stats['utilization_rate']}%\n")
                
                elif "semester_breakdown" in report_data:
                    f.write("SEMESTER BREAKDOWN\n")
                    f.write("Semester,Classes,Enrollment,Capacity,Utilization\n")
                    for semester, stats in report_data["semester_breakdown"].items():
                        utilization = stats.get("utilization", 0)
                        f.write(f"{semester},{stats['classes']},{stats['enrollment']},{stats['capacity']},{utilization}%\n")
            
            return {
                "success": True,
                "message": f"Report exported to {filename}",
                "filename": filename
            }
        except Exception as e:
            return {"success": False, "message": f"Export failed: {str(e)}"}

    def generate_dashboard_summary(self) -> Dict[str, Any]:
        """Generate dashboard summary with key metrics"""
        if not self.auth.has_permission(UserRole.ADMIN):
            return {"error": "Admin permission required"}
        
        faculty_list = self.db.get_all_faculty()
        all_classes = self.db.get_all_classes()
        all_students = self.db.get_all_students()
        
        # Calculate key metrics
        total_faculty = len(faculty_list)
        total_classes = len(all_classes)
        active_classes = len([c for c in all_classes if c.status.value == "active"])
        total_students = len(all_students)
        total_enrollment = sum(c.current_enrollment for c in all_classes)
        total_capacity = sum(c.max_capacity for c in all_classes)
        
        # Department count
        departments = len(set(f.department for f in faculty_list))
        
        # Utilization rate
        utilization_rate = (total_enrollment / total_capacity * 100) if total_capacity > 0 else 0
        
        return {
            "dashboard_type": "System Overview",
            "generated_at": datetime.now().isoformat(),
            "key_metrics": {
                "total_faculty": total_faculty,
                "total_students": total_students,
                "total_classes": total_classes,
                "active_classes": active_classes,
                "total_departments": departments,
                "total_enrollment": total_enrollment,
                "total_capacity": total_capacity,
                "utilization_rate": round(utilization_rate, 2)
            }
        }