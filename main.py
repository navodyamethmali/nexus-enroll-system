"""
Command Line Interface for the Nexus Enrollment System.
Demonstrates the "copy all items" functionality.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import Course, Student, Enrollment
from src.enrollment_system import EnrollmentSystem, EnrollmentObserver


def create_sample_data(system: EnrollmentSystem) -> None:
    """Create sample courses, students, and enrollments."""
    print("Creating sample data...")
    
    # Create sample courses
    courses = [
        Course("CS101", "Introduction to Computer Science", 3, "Dr. Smith"),
        Course("CS201", "Data Structures", 4, "Dr. Johnson"),
        Course("MATH101", "Calculus I", 4, "Dr. Brown"),
        Course("ENG101", "English Composition", 3, "Prof. Davis")
    ]
    
    for course in courses:
        system.add_course(course)
    
    # Create sample students
    students = [
        Student("STU001", "Alice Johnson", "alice@university.edu", 1),
        Student("STU002", "Bob Smith", "bob@university.edu", 2),
        Student("STU003", "Carol Wilson", "carol@university.edu", 1),
        Student("STU004", "David Brown", "david@university.edu", 3)
    ]
    
    for student in students:
        system.add_student(student)
    
    # Create sample enrollments
    enrollments = [
        ("STU001", "CS101"),
        ("STU001", "MATH101"),
        ("STU002", "CS201"),
        ("STU002", "ENG101"),
        ("STU003", "CS101"),
        ("STU004", "CS201")
    ]
    
    for student_id, course_id in enrollments:
        system.create_enrollment(student_id, course_id)
    
    print("Sample data created successfully!")


def display_system_status(system: EnrollmentSystem) -> None:
    """Display current system status."""
    stats = system.get_system_statistics()
    print(f"\n=== SYSTEM STATUS ===")
    print(f"Total Courses: {stats['total_courses']}")
    print(f"Total Students: {stats['total_students']}")
    print(f"Total Enrollments: {stats['total_enrollments']}")
    print(f"Total Items: {stats['total_items']}")


def display_items(system: EnrollmentSystem) -> None:
    """Display all items in the system."""
    print(f"\n=== COURSES ===")
    for course in system.list_all_courses():
        print(f"  {course}")
    
    print(f"\n=== STUDENTS ===")
    for student in system.list_all_students():
        print(f"  {student}")
    
    print(f"\n=== ENROLLMENTS ===")
    for enrollment in system.list_all_enrollments():
        print(f"  {enrollment}")


def demonstrate_copy_all_items(system: EnrollmentSystem) -> None:
    """Demonstrate the copy all items functionality."""
    print(f"\n" + "="*50)
    print("DEMONSTRATING 'COPY ALL ITEMS' FUNCTIONALITY")
    print("="*50)
    
    print("\nBefore copying:")
    display_system_status(system)
    
    print(f"\nExecuting 'copy all items' operation...")
    copied_items = system.copy_all_items()
    
    print(f"\nCopy operation completed!")
    print(f"Items copied:")
    print(f"  - Courses: {len(copied_items['courses'])}")
    print(f"  - Students: {len(copied_items['students'])}")
    print(f"  - Enrollments: {len(copied_items['enrollments'])}")
    
    print(f"\nCopied courses:")
    for course in copied_items['courses']:
        print(f"  {course}")
    
    print(f"\nCopied students:")
    for student in copied_items['students']:
        print(f"  {student}")
    
    print(f"\nCopied enrollments:")
    for enrollment in copied_items['enrollments']:
        print(f"  {enrollment}")
    
    # Add copied items back to system to demonstrate full functionality
    print(f"\nAdding copied items back to the system...")
    system.add_copied_items_to_system(copied_items)
    
    print(f"\nAfter adding copied items:")
    display_system_status(system)
    
    # Display copy history
    history = system.get_copy_history()
    print(f"\nCopy operation history:")
    for i, operation in enumerate(history, 1):
        print(f"  {i}. {operation['operation']} at {operation['timestamp']}")


def main():
    """Main application entry point."""
    print("Welcome to the Nexus Enrollment System")
    print("Demonstrating 'Copy All Items' functionality")
    print("="*50)
    
    # Create the enrollment system
    system = EnrollmentSystem()
    
    # Add an observer to monitor system events
    observer = EnrollmentObserver("SystemMonitor")
    system.add_observer(observer)
    
    # Create sample data
    create_sample_data(system)
    
    # Display initial system state
    print(f"\nInitial system state:")
    display_system_status(system)
    display_items(system)
    
    # Demonstrate the main functionality: copy all items
    demonstrate_copy_all_items(system)
    
    # Show final system state
    print(f"\nFinal system state (with copied items):")
    display_items(system)
    
    print(f"\n" + "="*50)
    print("COPY ALL ITEMS DEMONSTRATION COMPLETED!")
    print("="*50)


if __name__ == "__main__":
    main()