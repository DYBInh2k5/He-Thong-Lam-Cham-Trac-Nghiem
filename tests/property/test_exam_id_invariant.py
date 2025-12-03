"""Property-based tests for exam ID invariant on update.

Feature: multiple-choice-grading-system, Property 3: Exam ID invariant on update
"""

import tempfile
import shutil
from hypothesis import given, strategies as st, settings
from src.storage.file_storage import FileStorageManager
from src.business.exam_manager import ExamManager


@given(
    st.text(min_size=1, max_size=50),
    st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=48, max_codepoint=122
    )),
    st.text(min_size=1, max_size=50)  # New title for update
)
@settings(max_examples=100)
def test_exam_id_invariant_on_update(original_title, teacher_id, new_title):
    """
    Feature: multiple-choice-grading-system, Property 3: Exam ID invariant on update
    
    For any exam, updating the exam's information should preserve the 
    original exam_id unchanged.
    
    Validates: Requirements 1.3
    """
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Initialize storage and manager
        storage = FileStorageManager(base_path=temp_dir)
        manager = ExamManager(storage)
        
        # Create exam
        success, msg, exam_id = manager.create_exam(original_title, teacher_id)
        assert success, f"Failed to create exam: {msg}"
        
        # Add at least one question (required for validation)
        choices = {'A': 'Choice A', 'B': 'Choice B', 'C': 'Choice C', 'D': 'Choice D'}
        success, msg, q_id = manager.add_question(exam_id, "Test question", choices, 'A')
        assert success, f"Failed to add question: {msg}"
        
        # Store original exam_id
        original_exam_id = exam_id
        
        # Update exam with new title
        success, msg = manager.update_exam(exam_id, {'title': new_title})
        assert success, f"Failed to update exam: {msg}"
        
        # Get updated exam
        success, msg, exam_dict = manager.get_exam(exam_id)
        assert success, f"Failed to get exam: {msg}"
        
        # Verify exam_id is unchanged
        assert exam_dict['exam_id'] == original_exam_id, \
            f"Exam ID should not change: {original_exam_id} != {exam_dict['exam_id']}"
        
        # Verify title was updated
        assert exam_dict['title'] == new_title, \
            f"Title should be updated to '{new_title}', got '{exam_dict['title']}'"
    
    finally:
        # Clean up
        shutil.rmtree(temp_dir, ignore_errors=True)


@given(
    st.text(min_size=1, max_size=50),
    st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=48, max_codepoint=122
    )),
    st.lists(st.text(min_size=1, max_size=50), min_size=1, max_size=5)
)
@settings(max_examples=100)
def test_exam_id_invariant_on_multiple_updates(title, teacher_id, new_titles):
    """Test that exam ID remains unchanged after multiple updates."""
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Initialize storage and manager
        storage = FileStorageManager(base_path=temp_dir)
        manager = ExamManager(storage)
        
        # Create exam
        success, msg, exam_id = manager.create_exam(title, teacher_id)
        assert success, f"Failed to create exam: {msg}"
        
        # Add at least one question (required for validation)
        choices = {'A': 'Choice A', 'B': 'Choice B', 'C': 'Choice C', 'D': 'Choice D'}
        success, msg, q_id = manager.add_question(exam_id, "Test question", choices, 'A')
        assert success, f"Failed to add question: {msg}"
        
        # Store original exam_id
        original_exam_id = exam_id
        
        # Perform multiple updates
        for new_title in new_titles:
            success, msg = manager.update_exam(exam_id, {'title': new_title})
            assert success, f"Failed to update exam: {msg}"
            
            # Verify exam_id is still unchanged
            success, msg, exam_dict = manager.get_exam(exam_id)
            assert success, f"Failed to get exam: {msg}"
            assert exam_dict['exam_id'] == original_exam_id, \
                f"Exam ID should remain {original_exam_id} after update"
    
    finally:
        # Clean up
        shutil.rmtree(temp_dir, ignore_errors=True)
