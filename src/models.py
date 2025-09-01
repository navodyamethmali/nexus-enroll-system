"""
Core models for the Nexus Enrollment System.
Implements design patterns for a university course enrollment system.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime
import copy
import uuid


class Copyable(ABC):
    """Abstract base class for objects that can be copied."""
    
    @abstractmethod
    def copy(self) -> 'Copyable':
        """Create a copy of this object."""
        pass


class Course(Copyable):
    """Represents a university course."""
    
    def __init__(self, course_id: str, name: str, credits: int, 
                 instructor: str, capacity: int = 30):
        self.course_id = course_id
        self.name = name
        self.credits = credits
        self.instructor = instructor
        self.capacity = capacity
        self.enrolled_students: List[str] = []
        self.created_at = datetime.now()
    
    def copy(self) -> 'Course':
        """Create a copy of this course with a new ID."""
        new_course = Course(
            course_id=f"{self.course_id}_copy_{uuid.uuid4().hex[:8]}",
            name=f"{self.name} (Copy)",
            credits=self.credits,
            instructor=self.instructor,
            capacity=self.capacity
        )
        # Don't copy enrolled students to avoid conflicts
        return new_course
    
    def enroll_student(self, student_id: str) -> bool:
        """Enroll a student in this course."""
        if len(self.enrolled_students) < self.capacity and student_id not in self.enrolled_students:
            self.enrolled_students.append(student_id)
            return True
        return False
    
    def __str__(self) -> str:
        return f"Course({self.course_id}: {self.name}, Credits: {self.credits})"
    
    def __repr__(self) -> str:
        return self.__str__()


class Student(Copyable):
    """Represents a student in the enrollment system."""
    
    def __init__(self, student_id: str, name: str, email: str, year: int = 1):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.year = year
        self.enrolled_courses: List[str] = []
        self.created_at = datetime.now()
    
    def copy(self) -> 'Student':
        """Create a copy of this student with a new ID."""
        new_student = Student(
            student_id=f"{self.student_id}_copy_{uuid.uuid4().hex[:8]}",
            name=f"{self.name} (Copy)",
            email=f"copy_{self.email}",
            year=self.year
        )
        # Don't copy enrolled courses to avoid conflicts
        return new_student
    
    def enroll_in_course(self, course_id: str) -> bool:
        """Enroll this student in a course."""
        if course_id not in self.enrolled_courses:
            self.enrolled_courses.append(course_id)
            return True
        return False
    
    def __str__(self) -> str:
        return f"Student({self.student_id}: {self.name}, Year: {self.year})"
    
    def __repr__(self) -> str:
        return self.__str__()


class Enrollment(Copyable):
    """Represents an enrollment relationship between a student and course."""
    
    def __init__(self, enrollment_id: str, student_id: str, course_id: str, 
                 grade: Optional[str] = None):
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.course_id = course_id
        self.grade = grade
        self.enrollment_date = datetime.now()
        self.status = "active"  # active, completed, dropped
    
    def copy(self) -> 'Enrollment':
        """Create a copy of this enrollment with a new ID."""
        return Enrollment(
            enrollment_id=f"{self.enrollment_id}_copy_{uuid.uuid4().hex[:8]}",
            student_id=self.student_id,
            course_id=self.course_id,
            grade=self.grade
        )
    
    def set_grade(self, grade: str) -> None:
        """Set the grade for this enrollment."""
        self.grade = grade
        if grade in ['A', 'B', 'C', 'D', 'F']:
            self.status = "completed"
    
    def __str__(self) -> str:
        return f"Enrollment({self.enrollment_id}: {self.student_id} -> {self.course_id})"
    
    def __repr__(self) -> str:
        return self.__str__()