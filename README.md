# Faculty and Class Management System

A comprehensive Python-based automated system for managing faculty, classes, students, and enrollments in educational institutions.

## Features

### 🔐 Authentication & User Management
- Secure login system with role-based access control
- Admin, Faculty, and Student user roles
- Password hashing and user session management

### 👨‍🏫 Faculty Management
- Add, view, update, and deactivate faculty members
- Search faculty by name, department, or specialization
- Faculty workload tracking and reporting
- Department-wise faculty statistics
- Export faculty data to CSV

### 📚 Class Management
- Create and manage classes with course assignments
- Assign faculty to classes
- Track class capacity and enrollment
- Semester and academic year organization
- Room scheduling and utilization tracking
- Class status management (active/inactive/completed)

### 🎓 Student Management
- Student registration and profile management
- Student enrollment in classes
- Track student academic progress
- Search and filter students by various criteria
- Student statistics and reporting

### 📊 Reporting & Analytics
- Comprehensive faculty workload reports
- Class enrollment statistics
- Department performance analysis
- Room utilization reports
- Student enrollment trends
- Dashboard with key metrics
- Export reports to CSV format

## Installation

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Setup Instructions

1. **Clone or download the project files**
   ```bash
   # Ensure all Python files are in the same directory:
   # - main.py
   # - models.py
   # - database.py
   # - auth.py
   # - faculty_manager.py
   # - class_manager.py
   # - student_manager.py
   # - reports.py
   ```

2. **Run the application**
   ```bash
   python main.py
   ```

3. **Initial Setup**
   - The system will automatically create a default admin account
   - Default credentials: username=`admin`, password=`admin123`
   - Change the default password after first login

## Usage

### Getting Started

1. **Login**
   - Run `python main.py`
   - Use the default admin credentials or your custom credentials

2. **Add Sample Data**
   - Add courses first (required for creating classes)
   - Add faculty members
   - Add students
   - Create classes and assign faculty
   - Enroll students in classes

### Main Menu Options

#### Faculty Management
- **Add New Faculty**: Register new faculty members with complete information
- **View All Faculty**: Display all faculty members in a table format
- **Search Faculty**: Find faculty by name, department, or specialization
- **Update Faculty**: Modify faculty information
- **Faculty Workload Report**: View teaching load statistics
- **Export Faculty Data**: Download faculty data as CSV

#### Class Management
- **Add New Class**: Create new classes with course and faculty assignments
- **View All Classes**: Display all classes with enrollment information
- **Search Classes**: Find classes by various criteria
- **Update Class Information**: Modify class details
- **Change Class Status**: Activate/deactivate classes
- **Manage Enrollments**: Enroll/drop students from classes
- **Class Statistics**: View enrollment and capacity statistics
- **Export Class Data**: Download class data as CSV

#### Student Management
- **Add New Student**: Register new students
- **View All Students**: Display all students
- **Search Students**: Find students by various criteria
- **Update Student Information**: Modify student details
- **Manage Student Enrollments**: View and manage student class enrollments
- **Student Statistics**: View student distribution and statistics
- **Export Student Data**: Download student data as CSV

#### Reports & Analytics
- **Faculty Statistics**: Comprehensive faculty performance reports
- **Class Statistics**: Class enrollment and capacity analysis
- **Student Statistics**: Student distribution and enrollment trends
- **Enrollment Statistics**: Overall enrollment analysis
- **Department Statistics**: Department-wise performance metrics
- **Room Utilization**: Classroom usage analysis

## Database

The system uses SQLite database (`faculty_management.db`) which is automatically created on first run. The database includes the following tables:

- **users**: User accounts and authentication
- **faculty**: Faculty member information
- **students**: Student information
- **courses**: Course catalog
- **classes**: Class schedules and assignments
- **enrollments**: Student class enrollments
- **attendance**: Class attendance records

## File Structure

```
faculty-management-system/
├── main.py                 # Main application entry point
├── models.py              # Data models and enums
├── database.py            # Database operations and SQLite setup
├── auth.py                # Authentication and user management
├── faculty_manager.py     # Faculty management operations
├── class_manager.py       # Class management operations
├── student_manager.py     # Student management operations
├── reports.py             # Reporting and analytics
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── faculty_management.db  # SQLite database (created automatically)
```

## Security Features

- Password hashing using SHA-256
- Role-based access control
- Input validation and sanitization
- SQL injection prevention through parameterized queries

## Customization

### Adding New Features
1. Extend the data models in `models.py`
2. Add database operations in `database.py`
3. Create management functions in respective manager files
4. Add menu options in `main.py`

### Database Modifications
- Modify table schemas in `DatabaseManager.init_database()`
- Update data models accordingly
- Create migration scripts for existing data

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure write permissions in the application directory
   - Check if SQLite is properly installed

2. **Import Errors**
   - Ensure all Python files are in the same directory
   - Check Python version (3.7+ required)

3. **Permission Denied**
   - Run with appropriate user permissions
   - Check file system permissions

### Support

For issues or questions:
1. Check the error messages in the console
2. Verify all files are present and properly named
3. Ensure Python 3.7+ is installed
4. Check database file permissions

## Future Enhancements

- Web-based interface using Flask/Django
- Advanced reporting with charts and graphs
- Email notifications and alerts
- Grade management system
- Attendance tracking
- Course prerequisite management
- Advanced search and filtering
- Data backup and restore functionality
- Multi-language support

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.