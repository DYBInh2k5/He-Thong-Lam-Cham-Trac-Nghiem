"""Submission data model."""

from datetime import datetime
from typing import Dict, Optional, Tuple


class Submission:
    """Represents a student's submission for an exam."""
    
    def __init__(
        self,
        submission_id: str,
        exam_id: str,
        student_id: str,
        submitted_at: Optional[str] = None,
        answers: Optional[Dict[str, str]] = None
    ):
        self.submission_id = submission_id
        self.exam_id = exam_id
        self.student_id = student_id
        self.submitted_at = submitted_at or datetime.utcnow().isoformat() + 'Z'
        self.answers = answers or {}
    
    def save_answer(self, question_id: str, answer: str) -> Tuple[bool, str]:
        """Save an answer for a question.
        
        Args:
            question_id: ID of the question
            answer: Student's answer (A, B, C, or D)
        
        Returns:
            Tuple of (success, message)
        """
        # Validate answer
        if answer not in {'A', 'B', 'C', 'D'}:
            return False, "Đáp án phải là A, B, C hoặc D"
        
        self.answers[question_id] = answer
        return True, "Lưu câu trả lời thành công"
    
    def validate(self) -> Tuple[bool, str]:
        """Validate submission data.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.submission_id:
            return False, "Mã bài làm không được để trống"
        
        if not self.exam_id:
            return False, "Mã đề thi không được để trống"
        
        if not self.student_id:
            return False, "Mã học sinh không được để trống"
        
        # Validate all answers
        for question_id, answer in self.answers.items():
            if answer not in {'A', 'B', 'C', 'D'}:
                return False, f"Câu trả lời cho câu {question_id} không hợp lệ"
        
        return True, ""
    
    def to_dict(self) -> dict:
        """Convert submission to dictionary."""
        return {
            'submission_id': self.submission_id,
            'exam_id': self.exam_id,
            'student_id': self.student_id,
            'submitted_at': self.submitted_at,
            'answers': self.answers
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Submission':
        """Create submission from dictionary."""
        return cls(
            submission_id=data['submission_id'],
            exam_id=data['exam_id'],
            student_id=data['student_id'],
            submitted_at=data.get('submitted_at'),
            answers=data.get('answers', {})
        )
