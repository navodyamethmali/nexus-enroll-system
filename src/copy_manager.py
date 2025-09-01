"""
Copy manager implementing the Command pattern for copying operations.
Provides functionality to copy all items in the enrollment system.
"""
from typing import List, Dict, Any, Type, TypeVar
from abc import ABC, abstractmethod
from .models import Copyable, Course, Student, Enrollment

T = TypeVar('T', bound=Copyable)


class CopyCommand(ABC):
    """Abstract command for copy operations."""
    
    @abstractmethod
    def execute(self) -> List[Copyable]:
        """Execute the copy command."""
        pass


class CopyAllItemsCommand(CopyCommand):
    """Command to copy all items of a specific type."""
    
    def __init__(self, items: List[Copyable]):
        self.items = items
    
    def execute(self) -> List[Copyable]:
        """Copy all items and return the copies."""
        copied_items = []
        for item in self.items:
            copied_item = item.copy()
            copied_items.append(copied_item)
        return copied_items


class CopyManager:
    """
    Manager class that handles copying operations using the Command pattern.
    Implements the "copy all items" functionality.
    """
    
    def __init__(self):
        self.copy_history: List[Dict[str, Any]] = []
    
    def copy_all_courses(self, courses: List[Course]) -> List[Course]:
        """Copy all courses."""
        command = CopyAllItemsCommand(courses)
        copied_items = command.execute()
        
        # Record the operation
        self.copy_history.append({
            'operation': 'copy_all_courses',
            'original_count': len(courses),
            'copied_count': len(copied_items),
            'timestamp': self._get_timestamp()
        })
        
        return copied_items
    
    def copy_all_students(self, students: List[Student]) -> List[Student]:
        """Copy all students."""
        command = CopyAllItemsCommand(students)
        copied_items = command.execute()
        
        # Record the operation
        self.copy_history.append({
            'operation': 'copy_all_students',
            'original_count': len(students),
            'copied_count': len(copied_items),
            'timestamp': self._get_timestamp()
        })
        
        return copied_items
    
    def copy_all_enrollments(self, enrollments: List[Enrollment]) -> List[Enrollment]:
        """Copy all enrollments."""
        command = CopyAllItemsCommand(enrollments)
        copied_items = command.execute()
        
        # Record the operation
        self.copy_history.append({
            'operation': 'copy_all_enrollments',
            'original_count': len(enrollments),
            'copied_count': len(copied_items),
            'timestamp': self._get_timestamp()
        })
        
        return copied_items
    
    def copy_all_items(self, courses: List[Course], students: List[Student], 
                      enrollments: List[Enrollment]) -> Dict[str, List[Copyable]]:
        """
        Copy all items in the system: courses, students, and enrollments.
        This is the main implementation of the "copy all items" requirement.
        """
        result = {}
        
        # Copy all courses
        copied_courses = self.copy_all_courses(courses)
        result['courses'] = copied_courses
        
        # Copy all students
        copied_students = self.copy_all_students(students)
        result['students'] = copied_students
        
        # Copy all enrollments
        copied_enrollments = self.copy_all_enrollments(enrollments)
        result['enrollments'] = copied_enrollments
        
        # Record the comprehensive operation
        self.copy_history.append({
            'operation': 'copy_all_items',
            'courses_copied': len(copied_courses),
            'students_copied': len(copied_students),
            'enrollments_copied': len(copied_enrollments),
            'timestamp': self._get_timestamp()
        })
        
        return result
    
    def get_copy_history(self) -> List[Dict[str, Any]]:
        """Get the history of all copy operations."""
        return self.copy_history.copy()
    
    def _get_timestamp(self) -> str:
        """Get current timestamp as string."""
        from datetime import datetime
        return datetime.now().isoformat()


class CopyFactory:
    """Factory pattern implementation for creating copy managers."""
    
    @staticmethod
    def create_copy_manager() -> CopyManager:
        """Create a new copy manager instance."""
        return CopyManager()
    
    @staticmethod
    def create_batch_copy_manager() -> 'BatchCopyManager':
        """Create a batch copy manager for large operations."""
        return BatchCopyManager()


class BatchCopyManager(CopyManager):
    """Extended copy manager for batch operations."""
    
    def __init__(self):
        super().__init__()
        self.batch_size = 100
    
    def copy_all_items_in_batches(self, courses: List[Course], students: List[Student], 
                                 enrollments: List[Enrollment]) -> Dict[str, List[Copyable]]:
        """Copy all items in batches for better performance with large datasets."""
        result = {'courses': [], 'students': [], 'enrollments': []}
        
        # Process courses in batches
        for i in range(0, len(courses), self.batch_size):
            batch = courses[i:i + self.batch_size]
            batch_copies = self.copy_all_courses(batch)
            result['courses'].extend(batch_copies)
        
        # Process students in batches
        for i in range(0, len(students), self.batch_size):
            batch = students[i:i + self.batch_size]
            batch_copies = self.copy_all_students(batch)
            result['students'].extend(batch_copies)
        
        # Process enrollments in batches
        for i in range(0, len(enrollments), self.batch_size):
            batch = enrollments[i:i + self.batch_size]
            batch_copies = self.copy_all_enrollments(batch)
            result['enrollments'].extend(batch_copies)
        
        return result