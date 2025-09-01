# Nexus Enrollment System
University Course Enrolment System - A Modernization Project with Design Patterns

## Overview
The Nexus Enrollment System is a comprehensive university course enrollment management system that demonstrates modern software design patterns. The system implements a **"Copy All Items"** functionality that allows duplication of all enrollment system entities including courses, students, and enrollments.

## Key Features
- **Copy All Items**: Core functionality to duplicate all system entities
- **Design Patterns**: Implements Observer, Command, and Factory patterns
- **Comprehensive Testing**: Full test coverage for copy operations
- **CLI Interface**: Interactive demonstration of system capabilities

## Architecture
The system is built with the following components:

### Core Models (`src/models.py`)
- `Course`: Represents university courses with enrollment capacity
- `Student`: Represents students with enrollment tracking
- `Enrollment`: Represents student-course enrollment relationships
- `Copyable`: Abstract base class defining copy interface

### Copy Management (`src/copy_manager.py`)
- `CopyManager`: Implements Command pattern for copy operations
- `CopyAllItemsCommand`: Specific command for copying all items
- `CopyFactory`: Factory pattern for creating copy managers
- `BatchCopyManager`: Optimized copying for large datasets

### Enrollment System (`src/enrollment_system.py`)
- `EnrollmentSystem`: Main system implementing Observer pattern
- `EnrollmentObserver`: Observer for system event monitoring
- Integration of copy functionality with system management

## Usage

### Running the Application
```bash
python main.py
```

This will demonstrate the "copy all items" functionality by:
1. Creating sample courses, students, and enrollments
2. Displaying the initial system state
3. Executing the copy all items operation
4. Showing the copied items with unique identifiers
5. Adding copied items back to the system
6. Displaying the final state with doubled inventory

### Running Tests
```bash
python -m tests.test_copy_functionality
```

## Copy All Items Functionality

The main requirement "copy all items" is implemented through several layers:

1. **Individual Item Copying**: Each entity (Course, Student, Enrollment) implements the `Copyable` interface
2. **Batch Copying**: `CopyManager` provides methods to copy collections of items
3. **System-Level Copying**: `EnrollmentSystem.copy_all_items()` provides the main entry point
4. **Unique Identification**: All copied items receive new unique IDs to prevent conflicts

### Example Output
```
Before copying:
Total Courses: 4
Total Students: 4  
Total Enrollments: 6
Total Items: 14

Copy operation completed!
Items copied:
- Courses: 4
- Students: 4
- Enrollments: 6

After adding copied items:
Total Courses: 8
Total Students: 8
Total Enrollments: 12
Total Items: 28
```

## Design Patterns Used

### 1. Observer Pattern
- `EnrollmentSystem` notifies observers of system events
- `EnrollmentObserver` monitors copy operations and other activities

### 2. Command Pattern  
- `CopyCommand` encapsulates copy operations
- `CopyAllItemsCommand` implements specific copy all functionality

### 3. Factory Pattern
- `CopyFactory` creates appropriate copy manager instances
- Supports both standard and batch copy managers

### 4. Template Method Pattern
- `Copyable` abstract base class defines copy interface
- Each entity implements specific copy behavior

## Project Structure
```
nexus-enroll-system/
├── src/
│   ├── __init__.py
│   ├── models.py              # Core entity models
│   ├── copy_manager.py        # Copy functionality implementation
│   └── enrollment_system.py   # Main system with Observer pattern
├── tests/
│   └── test_copy_functionality.py  # Comprehensive tests
├── main.py                    # CLI demonstration application
├── requirements.txt           # Project dependencies
└── README.md                  # This documentation
```

## Requirements
- Python 3.7+
- No external dependencies (uses only Python standard library)

## Testing
The system includes comprehensive unit tests covering:
- Individual item copying
- Batch copying operations
- System-level copy all items functionality
- Copy history tracking
- Observer pattern notifications
- Factory pattern implementations
