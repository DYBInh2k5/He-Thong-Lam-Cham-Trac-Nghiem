"""Property-based tests for exam persistence.

Feature: multiple-choice-grading-system, Property 1: Exam persistence round-trip
"""

import tempfile
import shutil
from hypothesis import given, strategies as st, settings
from src.models.exam import Exam, Question
from src.storage.file_storage import FileStorageManager


# Strategy for generating valid questions
@st.composite
def question_strategy(draw):
    """Generate a valid question."""
    question_id = draw(st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=48, max_codepoint=122
    )))
    content = draw(st.text(min_size=1, max_size=200))
    
    choices = {
        'A': draw(st.text(min_size=1, max_size=100)),
        'B': draw(st.text(min_size=1, max_size=100)),
        'C': draw(st.text(min_size=1, max_size=100)),
        'D': draw(st.text(min_size=1, max_size=100))
    }
    
    correct_answer = draw(st.sampled_from(['A', 'B', 'C', 'D']))
    
    return Question(
        question_id=question_id,
        content=content,
        choices=choices,
        correct_answer=correct_answer
    )


# Strategy for generating valid exams
@st.composite
def exam_strategy(draw):
    """Generate a valid exam."""
    exam_id = draw(st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=48, max_codepoint=122
    )))
    title = draw(st.text(min_size=1, max_size=100))
    created_by = draw(st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=48, max_codepoint=122
    )))
    
    # Generate 1-10 unique questions
    num_questions = draw(st.integers(min_value=1, max_value=10))
    questions = []
    used_ids = set()
    
    for i in range(num_questions):
        question = draw(question_strategy())
        # Ensure unique question IDs
        while question.question_id in used_ids:
            question.question_id = f"{question.question_id}_{i}"
        used_ids.add(question.question_id)
        questions.append(question)
    
    return Exam(
        exam_id=exam_id,
        title=title,
        created_by=created_by,
        questions=questions
    )


@given(exam_strategy())
@settings(max_examples=100)
def test_exam_persistence_round_trip(exam):
    """
    Feature: multiple-choice-grading-system, Property 1: Exam persistence round-trip
    
    For any exam with valid data, saving then loading the exam should produce 
    an equivalent exam with all information preserved (exam_id, title, questions, 
    choices, correct answers).
    
    Validates: Requirements 1.1
    """
    # Create temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Initialize storage manager
        storage = FileStorageManager(base_path=temp_dir)
        
        # Convert exam to dict and save
        exam_dict = exam.to_dict()
        success = storage.save_exam(exam_dict)
        assert success, "Failed to save exam"
        
        # Load exam back
        loaded_dict = storage.load_exam(exam.exam_id)
        assert loaded_dict is not None, "Failed to load exam"
        
        # Convert back to Exam object
        loaded_exam = Exam.from_dict(loaded_dict)
        
        # Verify all fields are preserved
        assert loaded_exam.exam_id == exam.exam_id, "Exam ID not preserved"
        assert loaded_exam.title == exam.title, "Title not preserved"
        assert loaded_exam.created_by == exam.created_by, "Created by not preserved"
        assert len(loaded_exam.questions) == len(exam.questions), "Question count not preserved"
        
        # Verify each question
        for original_q, loaded_q in zip(exam.questions, loaded_exam.questions):
            assert loaded_q.question_id == original_q.question_id, "Question ID not preserved"
            assert loaded_q.content == original_q.content, "Question content not preserved"
            assert loaded_q.choices == original_q.choices, "Choices not preserved"
            assert loaded_q.correct_answer == original_q.correct_answer, "Correct answer not preserved"
    
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)
