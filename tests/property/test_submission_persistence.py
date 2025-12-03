"""Property-based tests for submission persistence.

Feature: multiple-choice-grading-system, Property 9: Submission round-trip
"""

import tempfile
import shutil
from hypothesis import given, strategies as st, settings
from src.models.submission import Submission
from src.storage.file_storage import FileStorageManager


# Strategy for generating valid submissions
@st.composite
def submission_strategy(draw):
    """Generate a valid submission."""
    submission_id = draw(st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=48, max_codepoint=122
    )))
    exam_id = draw(st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=48, max_codepoint=122
    )))
    student_id = draw(st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=48, max_codepoint=122
    )))
    
    # Generate random answers (question_id -> answer)
    num_answers = draw(st.integers(min_value=0, max_value=20))
    answers = {}
    for i in range(num_answers):
        question_id = f"Q{i+1}"
        answer = draw(st.sampled_from(['A', 'B', 'C', 'D']))
        answers[question_id] = answer
    
    return Submission(
        submission_id=submission_id,
        exam_id=exam_id,
        student_id=student_id,
        answers=answers
    )


@given(submission_strategy())
@settings(max_examples=100)
def test_submission_persistence_round_trip(submission):
    """
    Feature: multiple-choice-grading-system, Property 9: Submission round-trip
    
    For any valid submission with student_id, exam_id, and answers, saving then 
    loading should produce an equivalent submission with all data preserved.
    
    Validates: Requirements 3.3
    """
    # Create temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Initialize storage manager
        storage = FileStorageManager(base_path=temp_dir)
        
        # Convert submission to dict and save
        submission_dict = submission.to_dict()
        success = storage.save_submission(submission_dict)
        assert success, "Failed to save submission"
        
        # Load submission back
        loaded_dict = storage.load_submission(submission.submission_id)
        assert loaded_dict is not None, "Failed to load submission"
        
        # Convert back to Submission object
        loaded_submission = Submission.from_dict(loaded_dict)
        
        # Verify all fields are preserved
        assert loaded_submission.submission_id == submission.submission_id, "Submission ID not preserved"
        assert loaded_submission.exam_id == submission.exam_id, "Exam ID not preserved"
        assert loaded_submission.student_id == submission.student_id, "Student ID not preserved"
        assert loaded_submission.answers == submission.answers, "Answers not preserved"
    
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)
