"""Unit tests for ExamManager."""

import tempfile
import shutil
import pytest
from src.storage.file_storage import FileStorageManager
from src.business.exam_manager import ExamManager


@pytest.fixture
def manager():
    """Create a temporary exam manager for testing."""
    temp_dir = tempfile.mkdtemp()
    storage = FileStorageManager(base_path=temp_dir)
    exam_manager = ExamManager(storage)
    yield exam_manager
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_create_exam_success(manager):
    """Test creating an exam successfully."""
    success, msg, exam_id = manager.create_exam("Test Exam", "T001")
    
    assert success is True
    assert "thành công" in msg.lower()
    assert exam_id is not None
    assert exam_id.startswith("E")


def test_create_exam_empty_title(manager):
    """Test creating exam with empty title fails."""
    success, msg, exam_id = manager.create_exam("", "T001")
    
    assert success is False
    assert "tên đề thi" in msg.lower()
    assert exam_id is None


def test_create_exam_empty_teacher_id(manager):
    """Test creating exam with empty teacher ID fails."""
    success, msg, exam_id = manager.create_exam("Test Exam", "")
    
    assert success is False
    assert "giáo viên" in msg.lower()
    assert exam_id is None


def test_add_question_success(manager):
    """Test adding a question to an exam."""
    # Create exam first
    success, msg, exam_id = manager.create_exam("Test Exam", "T001")
    assert success is True
    
    # Add question
    choices = {'A': 'Answer A', 'B': 'Answer B', 'C': 'Answer C', 'D': 'Answer D'}
    success, msg, q_id = manager.add_question(exam_id, "What is 1+1?", choices, 'B')
    
    assert success is True
    assert "thành công" in msg.lower()
    assert q_id is not None


def test_add_question_to_nonexistent_exam(manager):
    """Test adding question to non-existent exam fails."""
    choices = {'A': 'Answer A', 'B': 'Answer B', 'C': 'Answer C', 'D': 'Answer D'}
    success, msg, q_id = manager.add_question("NONEXISTENT", "Question?", choices, 'A')
    
    assert success is False
    assert "không tồn tại" in msg.lower()
    assert q_id is None


def test_add_question_without_correct_answer(manager):
    """Test adding question without correct answer fails."""
    # Create exam
    success, msg, exam_id = manager.create_exam("Test Exam", "T001")
    assert success is True
    
    # Try to add question with invalid correct answer
    choices = {'A': 'Answer A', 'B': 'Answer B', 'C': 'Answer C', 'D': 'Answer D'}
    success, msg, q_id = manager.add_question(exam_id, "Question?", choices, 'E')
    
    assert success is False
    assert q_id is None


def test_add_question_missing_choice(manager):
    """Test adding question with missing choice fails."""
    # Create exam
    success, msg, exam_id = manager.create_exam("Test Exam", "T001")
    assert success is True
    
    # Try to add question with missing choice D
    choices = {'A': 'Answer A', 'B': 'Answer B', 'C': 'Answer C'}
    success, msg, q_id = manager.add_question(exam_id, "Question?", choices, 'A')
    
    assert success is False
    assert q_id is None


def test_update_exam_success(manager):
    """Test updating exam successfully."""
    # Create exam with question
    success, msg, exam_id = manager.create_exam("Original Title", "T001")
    assert success is True
    
    choices = {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'}
    success, msg, q_id = manager.add_question(exam_id, "Q?", choices, 'A')
    assert success is True
    
    # Update title
    success, msg = manager.update_exam(exam_id, {'title': 'New Title'})
    
    assert success is True
    assert "thành công" in msg.lower()
    
    # Verify update
    success, msg, exam_dict = manager.get_exam(exam_id)
    assert exam_dict['title'] == 'New Title'


def test_update_nonexistent_exam(manager):
    """Test updating non-existent exam fails."""
    success, msg = manager.update_exam("NONEXISTENT", {'title': 'New Title'})
    
    assert success is False
    assert "không tồn tại" in msg.lower()


def test_delete_exam_success(manager):
    """Test deleting exam successfully."""
    # Create exam with question
    success, msg, exam_id = manager.create_exam("Test Exam", "T001")
    assert success is True
    
    choices = {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'}
    success, msg, q_id = manager.add_question(exam_id, "Q?", choices, 'A')
    assert success is True
    
    # Delete exam
    success, msg = manager.delete_exam(exam_id)
    
    assert success is True
    assert "thành công" in msg.lower()
    
    # Verify deleted
    success, msg, exam_dict = manager.get_exam(exam_id)
    assert success is False
    assert exam_dict is None


def test_delete_nonexistent_exam(manager):
    """Test deleting non-existent exam fails."""
    success, msg = manager.delete_exam("NONEXISTENT")
    
    assert success is False
    assert "không tồn tại" in msg.lower()


def test_get_exam_success(manager):
    """Test getting an exam successfully."""
    # Create exam
    success, msg, exam_id = manager.create_exam("Test Exam", "T001")
    assert success is True
    
    # Get exam
    success, msg, exam_dict = manager.get_exam(exam_id)
    
    assert success is True
    assert exam_dict is not None
    assert exam_dict['exam_id'] == exam_id
    assert exam_dict['title'] == "Test Exam"


def test_get_nonexistent_exam(manager):
    """Test getting non-existent exam fails."""
    success, msg, exam_dict = manager.get_exam("NONEXISTENT")
    
    assert success is False
    assert exam_dict is None


def test_list_all_exams(manager):
    """Test listing all exams."""
    # Create multiple exams
    for i in range(3):
        success, msg, exam_id = manager.create_exam(f"Exam {i}", "T001")
        assert success is True
    
    # List exams
    success, msg, exams = manager.list_all_exams()
    
    assert success is True
    assert len(exams) == 3


def test_validate_exam_empty_questions(manager):
    """Test validation rejects exam with no questions."""
    exam_dict = {
        'exam_id': 'E001',
        'title': 'Test Exam',
        'created_by': 'T001',
        'created_at': '2024-01-01T00:00:00Z',
        'questions': []
    }
    
    is_valid, error_msg = manager.validate_exam(exam_dict)
    
    assert is_valid is False
    assert "câu hỏi" in error_msg.lower()
