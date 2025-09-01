"""
Unit tests for the copy all items functionality.
Tests the core requirement of copying all items in the enrollment system.
"""
import unittest
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import Course, Student, Enrollment
from src.copy_manager import CopyManager, CopyFactory, BatchCopyManager
from src.enrollment_system import EnrollmentSystem, EnrollmentObserver


class TestCopyAllItems(unittest.TestCase):
    """Test cases for the copy all items functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.system = EnrollmentSystem()
        self.copy_manager = CopyFactory.create_copy_manager()
        
        # Create sample data
        self.sample_course = Course("CS101", "Test Course", 3, "Dr. Test")
        self.sample_student = Student("STU001", "Test Student", "test@email.com")
        self.sample_enrollment = Enrollment("ENR001", "STU001", "CS101")
    
    def test_copy_single_course(self):
        """Test copying a single course."""
        copied_course = self.sample_course.copy()
        
        # Verify the copy is different but similar
        self.assertNotEqual(copied_course.course_id, self.sample_course.course_id)
        self.assertIn("copy", copied_course.course_id.lower())
        self.assertIn("Copy", copied_course.name)
        self.assertEqual(copied_course.credits, self.sample_course.credits)
        self.assertEqual(copied_course.instructor, self.sample_course.instructor)
        self.assertEqual(copied_course.capacity, self.sample_course.capacity)
    
    def test_copy_single_student(self):
        """Test copying a single student."""
        copied_student = self.sample_student.copy()
        
        # Verify the copy is different but similar
        self.assertNotEqual(copied_student.student_id, self.sample_student.student_id)
        self.assertIn("copy", copied_student.student_id.lower())
        self.assertIn("Copy", copied_student.name)
        self.assertIn("copy_", copied_student.email)
        self.assertEqual(copied_student.year, self.sample_student.year)
    
    def test_copy_single_enrollment(self):
        """Test copying a single enrollment."""
        copied_enrollment = self.sample_enrollment.copy()
        
        # Verify the copy is different but similar
        self.assertNotEqual(copied_enrollment.enrollment_id, self.sample_enrollment.enrollment_id)
        self.assertIn("copy", copied_enrollment.enrollment_id.lower())
        self.assertEqual(copied_enrollment.student_id, self.sample_enrollment.student_id)
        self.assertEqual(copied_enrollment.course_id, self.sample_enrollment.course_id)
    
    def test_copy_all_courses(self):
        """Test copying all courses."""
        courses = [
            Course("CS101", "Course 1", 3, "Dr. A"),
            Course("CS102", "Course 2", 4, "Dr. B"),
            Course("CS103", "Course 3", 3, "Dr. C")
        ]
        
        copied_courses = self.copy_manager.copy_all_courses(courses)
        
        self.assertEqual(len(copied_courses), len(courses))
        for i, copied_course in enumerate(copied_courses):
            self.assertNotEqual(copied_course.course_id, courses[i].course_id)
            self.assertIn("copy", copied_course.course_id.lower())
            self.assertIn("Copy", copied_course.name)
    
    def test_copy_all_students(self):
        """Test copying all students."""
        students = [
            Student("STU001", "Student 1", "s1@email.com"),
            Student("STU002", "Student 2", "s2@email.com"),
            Student("STU003", "Student 3", "s3@email.com")
        ]
        
        copied_students = self.copy_manager.copy_all_students(students)
        
        self.assertEqual(len(copied_students), len(students))
        for i, copied_student in enumerate(copied_students):
            self.assertNotEqual(copied_student.student_id, students[i].student_id)
            self.assertIn("copy", copied_student.student_id.lower())
            self.assertIn("Copy", copied_student.name)
    
    def test_copy_all_enrollments(self):
        """Test copying all enrollments."""
        enrollments = [
            Enrollment("ENR001", "STU001", "CS101"),
            Enrollment("ENR002", "STU002", "CS102"),
            Enrollment("ENR003", "STU003", "CS103")
        ]
        
        copied_enrollments = self.copy_manager.copy_all_enrollments(enrollments)
        
        self.assertEqual(len(copied_enrollments), len(enrollments))
        for i, copied_enrollment in enumerate(copied_enrollments):
            self.assertNotEqual(copied_enrollment.enrollment_id, enrollments[i].enrollment_id)
            self.assertIn("copy", copied_enrollment.enrollment_id.lower())
    
    def test_copy_all_items_main_functionality(self):
        """Test the main 'copy all items' functionality."""
        # Create test data
        courses = [
            Course("CS101", "Course 1", 3, "Dr. A"),
            Course("CS102", "Course 2", 4, "Dr. B")
        ]
        students = [
            Student("STU001", "Student 1", "s1@email.com"),
            Student("STU002", "Student 2", "s2@email.com")
        ]
        enrollments = [
            Enrollment("ENR001", "STU001", "CS101"),
            Enrollment("ENR002", "STU002", "CS102")
        ]
        
        # Execute copy all items
        result = self.copy_manager.copy_all_items(courses, students, enrollments)
        
        # Verify all items were copied
        self.assertIn('courses', result)
        self.assertIn('students', result)
        self.assertIn('enrollments', result)
        
        self.assertEqual(len(result['courses']), len(courses))
        self.assertEqual(len(result['students']), len(students))
        self.assertEqual(len(result['enrollments']), len(enrollments))
        
        # Verify copies are different from originals
        for i, copied_course in enumerate(result['courses']):
            self.assertNotEqual(copied_course.course_id, courses[i].course_id)
        
        for i, copied_student in enumerate(result['students']):
            self.assertNotEqual(copied_student.student_id, students[i].student_id)
        
        for i, copied_enrollment in enumerate(result['enrollments']):
            self.assertNotEqual(copied_enrollment.enrollment_id, enrollments[i].enrollment_id)
    
    def test_enrollment_system_copy_all_items(self):
        """Test copy all items through the enrollment system."""
        # Add items to the system
        course = Course("CS101", "Test Course", 3, "Dr. Test")
        student = Student("STU001", "Test Student", "test@email.com")
        
        self.system.add_course(course)
        self.system.add_student(student)
        enrollment = self.system.create_enrollment("STU001", "CS101")
        
        # Verify initial state
        self.assertEqual(len(self.system.list_all_courses()), 1)
        self.assertEqual(len(self.system.list_all_students()), 1)
        self.assertEqual(len(self.system.list_all_enrollments()), 1)
        
        # Copy all items
        copied_items = self.system.copy_all_items()
        
        # Verify copied items structure
        self.assertIn('courses', copied_items)
        self.assertIn('students', copied_items)
        self.assertIn('enrollments', copied_items)
        
        self.assertEqual(len(copied_items['courses']), 1)
        self.assertEqual(len(copied_items['students']), 1)
        self.assertEqual(len(copied_items['enrollments']), 1)
        
        # Verify copies are different
        copied_course = copied_items['courses'][0]
        copied_student = copied_items['students'][0]
        copied_enrollment = copied_items['enrollments'][0]
        
        self.assertNotEqual(copied_course.course_id, course.course_id)
        self.assertNotEqual(copied_student.student_id, student.student_id)
        self.assertNotEqual(copied_enrollment.enrollment_id, enrollment.enrollment_id)
    
    def test_copy_history_tracking(self):
        """Test that copy operations are tracked in history."""
        courses = [Course("CS101", "Course 1", 3, "Dr. A")]
        students = [Student("STU001", "Student 1", "s1@email.com")]
        
        # Perform copy operations
        self.copy_manager.copy_all_courses(courses)
        self.copy_manager.copy_all_students(students)
        
        history = self.copy_manager.get_copy_history()
        
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['operation'], 'copy_all_courses')
        self.assertEqual(history[1]['operation'], 'copy_all_students')
    
    def test_batch_copy_manager(self):
        """Test batch copying functionality."""
        batch_manager = CopyFactory.create_batch_copy_manager()
        
        # Create larger dataset
        courses = [Course(f"CS{i}", f"Course {i}", 3, f"Dr. {i}") for i in range(5)]
        students = [Student(f"STU{i:03d}", f"Student {i}", f"s{i}@email.com") for i in range(5)]
        enrollments = [Enrollment(f"ENR{i:03d}", f"STU{i:03d}", f"CS{i}") for i in range(5)]
        
        result = batch_manager.copy_all_items_in_batches(courses, students, enrollments)
        
        self.assertEqual(len(result['courses']), 5)
        self.assertEqual(len(result['students']), 5)
        self.assertEqual(len(result['enrollments']), 5)
    
    def test_observer_notifications_for_copy_operations(self):
        """Test that observers are notified of copy operations."""
        observer = EnrollmentObserver("TestObserver")
        self.system.add_observer(observer)
        
        # Add items and copy them
        course = Course("CS101", "Test Course", 3, "Dr. Test")
        self.system.add_course(course)
        
        copied_items = self.system.copy_all_items()
        
        # Check that observer received notifications
        notifications = observer.notifications
        self.assertTrue(len(notifications) >= 2)  # At least course_added and copy_all_items_completed
        
        # Find copy operation notification
        copy_notification = None
        for notification in notifications:
            if notification['event'] == 'copy_all_items_completed':
                copy_notification = notification
                break
        
        self.assertIsNotNone(copy_notification)
        self.assertEqual(copy_notification['data']['courses_copied'], 1)


class TestCopyFactory(unittest.TestCase):
    """Test the copy factory pattern implementation."""
    
    def test_create_copy_manager(self):
        """Test creating a standard copy manager."""
        manager = CopyFactory.create_copy_manager()
        self.assertIsInstance(manager, CopyManager)
    
    def test_create_batch_copy_manager(self):
        """Test creating a batch copy manager."""
        manager = CopyFactory.create_batch_copy_manager()
        self.assertIsInstance(manager, BatchCopyManager)
        self.assertIsInstance(manager, CopyManager)  # Should inherit from CopyManager


if __name__ == '__main__':
    unittest.main()