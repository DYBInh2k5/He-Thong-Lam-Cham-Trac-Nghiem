"""Property-based tests for UTF-8 encoding preservation.

Feature: multiple-choice-grading-system, Property 25: UTF-8 encoding preservation
"""

import tempfile
import shutil
from hypothesis import given, strategies as st, settings
from src.models.exam import Exam, Question
from src.storage.file_storage import FileStorageManager


# Strategy for generating Vietnamese text
vietnamese_chars = 'àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ'

@st.composite
def vietnamese_text_strategy(draw):
    """Generate text with Vietnamese characters."""
    # Mix Vietnamese characters with ASCII
    text = draw(st.text(
        alphabet=st.characters(
            whitelist_categories=('Lu', 'Ll', 'Nd', 'Zs'),
            whitelist_characters=vietnamese_chars
        ),
        min_size=1,
        max_size=100
    ))
    return text


@st.composite
def exam_with_vietnamese_strategy(draw):
    """Generate an exam with Vietnamese text."""
    exam_id = draw(st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=48, max_codepoint=122
    )))
    
    # Title with Vietnamese
    title = draw(vietnamese_text_strategy())
    
    created_by = draw(st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=48, max_codepoint=122
    )))
    
    # Generate questions with Vietnamese content
    num_questions = draw(st.integers(min_value=1, max_value=5))
    questions = []
    
    for i in range(num_questions):
        question_id = f"Q{i+1}"
        content = draw(vietnamese_text_strategy())
        
        choices = {
            'A': draw(vietnamese_text_strategy()),
            'B': draw(vietnamese_text_strategy()),
            'C': draw(vietnamese_text_strategy()),
            'D': draw(vietnamese_text_strategy())
        }
        
        correct_answer = draw(st.sampled_from(['A', 'B', 'C', 'D']))
        
        question = Question(
            question_id=question_id,
            content=content,
            choices=choices,
            correct_answer=correct_answer
        )
        questions.append(question)
    
    return Exam(
        exam_id=exam_id,
        title=title,
        created_by=created_by,
        questions=questions
    )


@given(exam_with_vietnamese_strategy())
@settings(max_examples=100)
def test_utf8_encoding_preservation(exam):
    """
    Feature: multiple-choice-grading-system, Property 25: UTF-8 encoding preservation
    
    For any data containing Vietnamese characters, saving then loading should 
    preserve all characters correctly without encoding errors.
    
    Validates: Requirements 10.4
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
        
        # Verify Vietnamese characters are preserved in title
        assert loaded_exam.title == exam.title, f"Title not preserved: expected '{exam.title}', got '{loaded_exam.title}'"
        
        # Verify Vietnamese characters in questions
        for original_q, loaded_q in zip(exam.questions, loaded_exam.questions):
            assert loaded_q.content == original_q.content, \
                f"Question content not preserved: expected '{original_q.content}', got '{loaded_q.content}'"
            
            # Check all choices
            for choice_key in ['A', 'B', 'C', 'D']:
                assert loaded_q.choices[choice_key] == original_q.choices[choice_key], \
                    f"Choice {choice_key} not preserved: expected '{original_q.choices[choice_key]}', got '{loaded_q.choices[choice_key]}'"
    
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)
