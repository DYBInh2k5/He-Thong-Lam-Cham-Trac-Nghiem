"""Property-based tests for adding questions to exams.

Feature: multiple-choice-grading-system, Property 2: Adding questions increases count
"""

import tempfile
import shutil
from hypothesis import given, strategies as st, settings
from src.models.exam import Exam, Question
from src.storage.file_storage import FileStorageManager
from src.business.exam_manager import ExamManager


@st.composite
def valid_question_data_strategy(draw):
    """Generate valid question data."""
    content = draw(st.text(min_size=1, max_size=100))
    choices = {
        'A': draw(st.text(min_size=1, max_size=50)),
        'B': draw(st.text(min_size=1, max_size=50)),
        'C': draw(st.text(min_size=1, max_size=50)),
        'D': draw(st.text(min_size=1, max_size=50))
    }
    correct_answer = draw(st.sampled_from(['A', 'B', 'C', 'D']))
    
    return content, choices, correct_answer


@given(
    st.text(min_size=1, max_size=50),
    st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=48, max_codepoint=122
    )),
    valid_question_data_strategy()
)
@settings(max_examples=100)
def test_adding_question_increases_count(title, teacher_id, question_data):
    """
    Feature: multiple-choice-grading-system, Property 2: Adding questions increases count
    
    For any exam and valid question, adding the question to the exam should 
    increase the question count by exactly one.
    
    Validates: Requirements 1.2
    """
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Initialize storage and manager
        storage = FileStorageManager(base_path=temp_dir)
        manager = ExamManager(storage)
        
        # Create exam
        success, msg, exam_id = manager.create_exam(title, teacher_id)
        assert success, f"Failed to create exam: {msg}"
        
        # Get initial question count
        success, msg, exam_dict = manager.get_exam(exam_id)
        assert success, f"Failed to get exam: {msg}"
        initial_count = len(exam_dict['questions'])
        
        # Add question
        content, choices, correct_answer = question_data
        success, msg, question_id = manager.add_question(
            exam_id, content, choices, correct_answer
        )
        assert success, f"Failed to add question: {msg}"
        
        # Get updated question count
        success, msg, exam_dict = manager.get_exam(exam_id)
        assert success, f"Failed to get exam: {msg}"
        new_count = len(exam_dict['questions'])
        
        # Verify count increased by exactly one
        assert new_count == initial_count + 1, \
            f"Question count should increase by 1: {initial_count} -> {new_count}"
    
    finally:
        # Clean up
        shutil.rmtree(temp_dir, ignore_errors=True)


@given(
    st.text(min_size=1, max_size=50),
    st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=48, max_codepoint=122
    )),
    st.lists(valid_question_data_strategy(), min_size=1, max_size=10)
)
@settings(max_examples=100)
def test_adding_multiple_questions_increases_count_correctly(title, teacher_id, questions_data):
    """Test that adding multiple questions increases count correctly."""
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Initialize storage and manager
        storage = FileStorageManager(base_path=temp_dir)
        manager = ExamManager(storage)
        
        # Create exam
        success, msg, exam_id = manager.create_exam(title, teacher_id)
        assert success, f"Failed to create exam: {msg}"
        
        # Add multiple questions
        for content, choices, correct_answer in questions_data:
            success, msg, question_id = manager.add_question(
                exam_id, content, choices, correct_answer
            )
            assert success, f"Failed to add question: {msg}"
        
        # Get final question count
        success, msg, exam_dict = manager.get_exam(exam_id)
        assert success, f"Failed to get exam: {msg}"
        final_count = len(exam_dict['questions'])
        
        # Verify count matches number of questions added
        assert final_count == len(questions_data), \
            f"Question count should be {len(questions_data)}, got {final_count}"
    
    finally:
        # Clean up
        shutil.rmtree(temp_dir, ignore_errors=True)
