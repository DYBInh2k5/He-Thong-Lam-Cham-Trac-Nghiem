"""Property-based tests for immediate persistence.

Feature: multiple-choice-grading-system, Property 24: Immediate persistence
"""

import tempfile
import shutil
import os
import json
from hypothesis import given, strategies as st, settings
from src.models.exam import Exam, Question
from src.storage.file_storage import FileStorageManager


@st.composite
def simple_exam_strategy(draw):
    """Generate a simple exam for testing."""
    exam_id = draw(st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=48, max_codepoint=122
    )))
    title = draw(st.text(min_size=1, max_size=50))
    created_by = draw(st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=48, max_codepoint=122
    )))
    
    # Create one simple question
    question = Question(
        question_id="Q1",
        content=draw(st.text(min_size=1, max_size=50)),
        choices={'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd'},
        correct_answer='A'
    )
    
    return Exam(
        exam_id=exam_id,
        title=title,
        created_by=created_by,
        questions=[question]
    )


@given(simple_exam_strategy())
@settings(max_examples=100)
def test_immediate_persistence_writes_to_file(exam):
    """
    Feature: multiple-choice-grading-system, Property 24: Immediate persistence
    
    For any data modification operation, the changes should be immediately 
    written to the corresponding file.
    
    Validates: Requirements 10.1
    """
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Initialize storage manager
        storage = FileStorageManager(base_path=temp_dir)
        
        # Save exam
        exam_dict = exam.to_dict()
        success = storage.save_exam(exam_dict)
        assert success, "Failed to save exam"
        
        # Immediately check if file exists (without using storage.load_exam)
        file_path = os.path.join(temp_dir, 'exams', f'{exam.exam_id}.json')
        assert os.path.exists(file_path), "File should exist immediately after save"
        
        # Verify file content is correct
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = json.load(f)
        
        assert file_content['exam_id'] == exam.exam_id, "Exam ID should be persisted"
        assert file_content['title'] == exam.title, "Title should be persisted"
        assert len(file_content['questions']) == len(exam.questions), "Questions should be persisted"
    
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)


@given(
    st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=48, max_codepoint=122
    )),
    st.text(min_size=1, max_size=50)
)
@settings(max_examples=100)
def test_immediate_persistence_for_all_entity_types(entity_id, name):
    """Test that all entity types are persisted immediately."""
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Initialize storage manager
        storage = FileStorageManager(base_path=temp_dir)
        
        # Test user persistence
        user_dict = {
            'user_id': entity_id,
            'name': name,
            'role': 'student',
            'created_at': '2024-01-01T00:00:00Z'
        }
        success = storage.save_user(user_dict)
        assert success, "Failed to save user"
        
        user_file = os.path.join(temp_dir, 'users', f'{entity_id}.json')
        assert os.path.exists(user_file), "User file should exist immediately"
        
        # Test submission persistence
        submission_dict = {
            'submission_id': entity_id,
            'exam_id': 'E001',
            'student_id': 'S001',
            'submitted_at': '2024-01-01T00:00:00Z',
            'answers': {}
        }
        success = storage.save_submission(submission_dict)
        assert success, "Failed to save submission"
        
        submission_file = os.path.join(temp_dir, 'submissions', f'{entity_id}.json')
        assert os.path.exists(submission_file), "Submission file should exist immediately"
        
        # Test result persistence
        result_dict = {
            'result_id': entity_id,
            'submission_id': 'SUB001',
            'exam_id': 'E001',
            'student_id': 'S001',
            'score': 10.0,
            'total_questions': 10,
            'correct_answers': 10,
            'wrong_answers': 0,
            'graded_at': '2024-01-01T00:00:00Z',
            'details': []
        }
        success = storage.save_result(result_dict)
        assert success, "Failed to save result"
        
        result_file = os.path.join(temp_dir, 'results', f'{entity_id}.json')
        assert os.path.exists(result_file), "Result file should exist immediately"
    
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)
