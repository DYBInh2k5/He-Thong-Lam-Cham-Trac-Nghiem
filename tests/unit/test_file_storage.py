"""Unit tests for FileStorageManager."""

import tempfile
import shutil
import os
import json
import pytest
from src.storage.file_storage import FileStorageManager


@pytest.fixture
def storage():
    """Create a temporary storage manager for testing."""
    temp_dir = tempfile.mkdtemp()
    storage_manager = FileStorageManager(base_path=temp_dir)
    yield storage_manager
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_save_and_load_exam(storage):
    """Test saving and loading an exam."""
    exam = {
        'exam_id': 'E001',
        'title': 'Test Exam',
        'created_by': 'T001',
        'created_at': '2024-01-01T00:00:00Z',
        'questions': []
    }
    
    # Save exam
    assert storage.save_exam(exam) is True
    
    # Load exam
    loaded = storage.load_exam('E001')
    assert loaded is not None
    assert loaded['exam_id'] == 'E001'
    assert loaded['title'] == 'Test Exam'


def test_list_exams(storage):
    """Test listing all exams."""
    # Save multiple exams
    for i in range(3):
        exam = {
            'exam_id': f'E{i:03d}',
            'title': f'Exam {i}',
            'created_by': 'T001',
            'created_at': '2024-01-01T00:00:00Z',
            'questions': []
        }
        storage.save_exam(exam)
    
    # List exams
    exams = storage.list_exams()
    assert len(exams) == 3
    exam_ids = [e['exam_id'] for e in exams]
    assert 'E000' in exam_ids
    assert 'E001' in exam_ids
    assert 'E002' in exam_ids


def test_delete_exam(storage):
    """Test deleting an exam."""
    exam = {
        'exam_id': 'E001',
        'title': 'Test Exam',
        'created_by': 'T001',
        'created_at': '2024-01-01T00:00:00Z',
        'questions': []
    }
    
    # Save and delete
    storage.save_exam(exam)
    assert storage.delete_exam('E001') is True
    
    # Verify deleted
    assert storage.load_exam('E001') is None


def test_save_and_load_user(storage):
    """Test saving and loading a user."""
    user = {
        'user_id': 'U001',
        'name': 'Test User',
        'role': 'student',
        'created_at': '2024-01-01T00:00:00Z'
    }
    
    # Save user
    assert storage.save_user(user) is True
    
    # Load user
    loaded = storage.load_user('U001')
    assert loaded is not None
    assert loaded['user_id'] == 'U001'
    assert loaded['name'] == 'Test User'


def test_list_users_with_filter(storage):
    """Test listing users with role filter."""
    # Save users with different roles
    for i in range(3):
        user = {
            'user_id': f'U{i:03d}',
            'name': f'User {i}',
            'role': 'teacher' if i % 2 == 0 else 'student',
            'created_at': '2024-01-01T00:00:00Z'
        }
        storage.save_user(user)
    
    # List all users
    all_users = storage.list_users()
    assert len(all_users) == 3
    
    # List only teachers
    teachers = storage.list_users(role='teacher')
    assert len(teachers) == 2
    
    # List only students
    students = storage.list_users(role='student')
    assert len(students) == 1


def test_list_submissions_with_filters(storage):
    """Test listing submissions with filters."""
    # Save submissions
    submissions = [
        {'submission_id': 'S001', 'exam_id': 'E001', 'student_id': 'ST001', 'submitted_at': '2024-01-01T00:00:00Z', 'answers': {}},
        {'submission_id': 'S002', 'exam_id': 'E001', 'student_id': 'ST002', 'submitted_at': '2024-01-01T00:00:00Z', 'answers': {}},
        {'submission_id': 'S003', 'exam_id': 'E002', 'student_id': 'ST001', 'submitted_at': '2024-01-01T00:00:00Z', 'answers': {}},
    ]
    
    for sub in submissions:
        storage.save_submission(sub)
    
    # List all
    all_subs = storage.list_submissions()
    assert len(all_subs) == 3
    
    # Filter by exam_id
    exam1_subs = storage.list_submissions(exam_id='E001')
    assert len(exam1_subs) == 2
    
    # Filter by student_id
    student1_subs = storage.list_submissions(student_id='ST001')
    assert len(student1_subs) == 2


def test_import_export_json(storage):
    """Test JSON import/export."""
    exam = {
        'exam_id': 'E001',
        'title': 'Test Exam',
        'created_by': 'T001',
        'created_at': '2024-01-01T00:00:00Z',
        'questions': []
    }
    
    # Export to JSON
    temp_file = os.path.join(storage.base_path, 'test_export.json')
    assert storage.export_to_json(exam, temp_file) is True
    
    # Verify file exists
    assert os.path.exists(temp_file)
    
    # Import from JSON
    assert storage.import_from_json(temp_file, 'exam') is True
    
    # Verify imported
    loaded = storage.load_exam('E001')
    assert loaded is not None
    assert loaded['title'] == 'Test Exam'


def test_import_from_csv(storage):
    """Test CSV import."""
    # Create a test CSV file
    csv_content = """question_id,content,choice_A,choice_B,choice_C,choice_D,correct_answer
Q001,What is 1+1?,1,2,3,4,B
Q002,What is 2+2?,2,3,4,5,C
"""
    
    csv_file = os.path.join(storage.base_path, 'test.csv')
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write(csv_content)
    
    # Import CSV
    result = storage.import_from_csv(csv_file)
    assert result is not None
    assert 'questions' in result
    assert len(result['questions']) == 2
    
    # Verify first question
    q1 = result['questions'][0]
    assert q1['question_id'] == 'Q001'
    assert q1['content'] == 'What is 1+1?'
    assert q1['correct_answer'] == 'B'


def test_export_to_csv(storage):
    """Test CSV export."""
    data = [
        {'id': '1', 'name': 'Item 1', 'value': '100'},
        {'id': '2', 'name': 'Item 2', 'value': '200'}
    ]
    
    csv_file = os.path.join(storage.base_path, 'export.csv')
    assert storage.export_to_csv(data, csv_file) is True
    
    # Verify file exists and has content
    assert os.path.exists(csv_file)
    with open(csv_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert 'id,name,value' in content
        assert 'Item 1' in content


def test_directory_creation(storage):
    """Test that all required directories are created."""
    required_dirs = ['exams', 'submissions', 'results', 'users']
    for dir_name in required_dirs:
        dir_path = os.path.join(storage.base_path, dir_name)
        assert os.path.exists(dir_path)
        assert os.path.isdir(dir_path)


def test_utf8_encoding(storage):
    """Test UTF-8 encoding with Vietnamese characters."""
    exam = {
        'exam_id': 'E001',
        'title': 'Đề thi Toán học',
        'created_by': 'GV001',
        'created_at': '2024-01-01T00:00:00Z',
        'questions': [{
            'question_id': 'Q001',
            'content': 'Câu hỏi tiếng Việt có dấu',
            'choices': {
                'A': 'Đáp án A',
                'B': 'Đáp án B',
                'C': 'Đáp án C',
                'D': 'Đáp án D'
            },
            'correct_answer': 'A'
        }]
    }
    
    # Save and load
    storage.save_exam(exam)
    loaded = storage.load_exam('E001')
    
    # Verify Vietnamese characters preserved
    assert loaded['title'] == 'Đề thi Toán học'
    assert loaded['questions'][0]['content'] == 'Câu hỏi tiếng Việt có dấu'
    assert loaded['questions'][0]['choices']['A'] == 'Đáp án A'
