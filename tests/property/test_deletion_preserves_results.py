"""Property-based tests for deletion preserving results.

Feature: multiple-choice-grading-system, Property 4: Deletion preserves related results
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
    ))
)
@settings(max_examples=100)
def test_deletion_preserves_related_results(title, teacher_id):
    """
    Feature: multiple-choice-grading-system, Property 4: Deletion preserves related results
    
    For any exam with associated results, deleting the exam should remove 
    the exam but keep all related result records intact.
    
    Validates: Requirements 1.4
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
        
        # Add a question
        choices = {'A': 'Choice A', 'B': 'Choice B', 'C': 'Choice C', 'D': 'Choice D'}
        success, msg, q_id = manager.add_question(exam_id, "Test question", choices, 'A')
        assert success, f"Failed to add question: {msg}"
        
        # Create some related results (manually for now, since GradingEngine not yet implemented)
        result1 = {
            'result_id': 'R001',
            'submission_id': 'S001',
            'exam_id': exam_id,
            'student_id': 'ST001',
            'score': 10.0,
            'total_questions': 1,
            'correct_answers': 1,
            'wrong_answers': 0,
            'graded_at': '2024-01-01T00:00:00Z',
            'details': []
        }
        result2 = {
            'result_id': 'R002',
            'submission_id': 'S002',
            'exam_id': exam_id,
            'student_id': 'ST002',
            'score': 5.0,
            'total_questions': 1,
            'correct_answers': 0,
            'wrong_answers': 1,
            'graded_at': '2024-01-01T00:00:00Z',
            'details': []
        }
        
        storage.save_result(result1)
        storage.save_result(result2)
        
        # Verify results exist before deletion
        results_before = storage.list_results(exam_id=exam_id)
        assert len(results_before) == 2, "Should have 2 results before deletion"
        
        # Delete exam
        success, msg = manager.delete_exam(exam_id)
        assert success, f"Failed to delete exam: {msg}"
        
        # Verify exam is deleted
        success, msg, exam_dict = manager.get_exam(exam_id)
        assert not success, "Exam should be deleted"
        assert exam_dict is None, "Exam dict should be None"
        
        # Verify results are still there
        results_after = storage.list_results(exam_id=exam_id)
        assert len(results_after) == 2, "Results should be preserved after exam deletion"
        
        # Verify result IDs are the same
        result_ids_before = {r['result_id'] for r in results_before}
        result_ids_after = {r['result_id'] for r in results_after}
        assert result_ids_before == result_ids_after, "Result IDs should be unchanged"
    
    finally:
        # Clean up
        shutil.rmtree(temp_dir, ignore_errors=True)
