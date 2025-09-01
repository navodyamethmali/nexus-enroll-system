"""
Enrollment system implementing the Observer pattern and managing all entities.
"""
from typing import List, Dict, Optional
from abc import ABC, abstractmethod
from .models import Course, Student, Enrollment
from .copy_manager import CopyManager, CopyFactory


class Observer(ABC):
    """Observer interface for the Observer pattern."""
    
    @abstractmethod
    def update(self, event: str, data: Dict) -> None:
        """Handle notification of system events."""
        pass


class EnrollmentObserver(Observer):
    """Observer for enrollment events."""
    
    def __init__(self, name: str):
        self.name = name
        self.notifications: List[Dict] = []
    
    def update(self, event: str, data: Dict) -> None:
        """Record enrollment-related events."""
        notification = {
            'observer': self.name,
            'event': event,
            'data': data,
            'timestamp': self._get_timestamp()
        }
        self.notifications.append(notification)
        print(f"[{self.name}] {event}: {data}")
    
    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()


class EnrollmentSystem:
    """
    Main enrollment system implementing the Observer pattern.
    Manages courses, students, and enrollments with copy functionality.
    """
    
    def __init__(self):
        self.courses: Dict[str, Course] = {}
        self.students: Dict[str, Student] = {}
        self.enrollments: Dict[str, Enrollment] = {}
        self.observers: List[Observer] = []
        self.copy_manager = CopyFactory.create_copy_manager()
    
    def add_observer(self, observer: Observer) -> None:
        """Add an observer to the system."""
        self.observers.append(observer)
    
    def remove_observer(self, observer: Observer) -> None:
        """Remove an observer from the system."""
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notify_observers(self, event: str, data: Dict) -> None:
        """Notify all observers of an event."""
        for observer in self.observers:
            observer.update(event, data)
    
    def add_course(self, course: Course) -> None:
        """Add a course to the system."""
        self.courses[course.course_id] = course
        self.notify_observers('course_added', {
            'course_id': course.course_id,
            'name': course.name
        })
    
    def add_student(self, student: Student) -> None:
        """Add a student to the system."""
        self.students[student.student_id] = student
        self.notify_observers('student_added', {
            'student_id': student.student_id,
            'name': student.name
        })
    
    def create_enrollment(self, student_id: str, course_id: str) -> Optional[Enrollment]:
        """Create an enrollment between a student and course."""
        if student_id not in self.students:
            return None
        if course_id not in self.courses:
            return None
        
        student = self.students[student_id]
        course = self.courses[course_id]
        
        # Check if enrollment already exists
        existing_enrollment = None
        for enrollment in self.enrollments.values():
            if enrollment.student_id == student_id and enrollment.course_id == course_id:
                existing_enrollment = enrollment
                break
        
        if existing_enrollment:
            return existing_enrollment
        
        # Create new enrollment
        enrollment_id = f"ENR_{student_id}_{course_id}"
        enrollment = Enrollment(enrollment_id, student_id, course_id)
        
        # Update both student and course
        if student.enroll_in_course(course_id) and course.enroll_student(student_id):
            self.enrollments[enrollment_id] = enrollment
            self.notify_observers('enrollment_created', {
                'enrollment_id': enrollment_id,
                'student_id': student_id,
                'course_id': course_id
            })
            return enrollment
        
        return None
    
    def copy_all_items(self) -> Dict[str, List]:
        """
        Copy all items in the system.
        This is the main implementation of the "copy all items" requirement.
        """
        courses_list = list(self.courses.values())
        students_list = list(self.students.values())
        enrollments_list = list(self.enrollments.values())
        
        copied_items = self.copy_manager.copy_all_items(
            courses_list, students_list, enrollments_list
        )
        
        # Notify observers about the copy operation
        self.notify_observers('copy_all_items_completed', {
            'courses_copied': len(copied_items['courses']),
            'students_copied': len(copied_items['students']),
            'enrollments_copied': len(copied_items['enrollments'])
        })
        
        return copied_items
    
    def add_copied_items_to_system(self, copied_items: Dict[str, List]) -> None:
        """Add copied items back to the system."""
        # Add copied courses
        for course in copied_items['courses']:
            self.add_course(course)
        
        # Add copied students
        for student in copied_items['students']:
            self.add_student(student)
        
        # Add copied enrollments
        for enrollment in copied_items['enrollments']:
            self.enrollments[enrollment.enrollment_id] = enrollment
        
        self.notify_observers('copied_items_added_to_system', {
            'total_items_added': (
                len(copied_items['courses']) + 
                len(copied_items['students']) + 
                len(copied_items['enrollments'])
            )
        })
    
    def get_system_statistics(self) -> Dict[str, int]:
        """Get statistics about the current system state."""
        return {
            'total_courses': len(self.courses),
            'total_students': len(self.students),
            'total_enrollments': len(self.enrollments),
            'total_items': len(self.courses) + len(self.students) + len(self.enrollments)
        }
    
    def get_copy_history(self) -> List[Dict]:
        """Get the history of copy operations."""
        return self.copy_manager.get_copy_history()
    
    def get_course(self, course_id: str) -> Optional[Course]:
        """Get a course by ID."""
        return self.courses.get(course_id)
    
    def get_student(self, student_id: str) -> Optional[Student]:
        """Get a student by ID."""
        return self.students.get(student_id)
    
    def get_enrollment(self, enrollment_id: str) -> Optional[Enrollment]:
        """Get an enrollment by ID."""
        return self.enrollments.get(enrollment_id)
    
    def list_all_courses(self) -> List[Course]:
        """Get all courses in the system."""
        return list(self.courses.values())
    
    def list_all_students(self) -> List[Student]:
        """Get all students in the system."""
        return list(self.students.values())
    
    def list_all_enrollments(self) -> List[Enrollment]:
        """Get all enrollments in the system."""
        return list(self.enrollments.values())