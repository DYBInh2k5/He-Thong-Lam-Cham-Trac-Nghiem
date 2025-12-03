"""Result data model."""

from datetime import datetime
from typing import List, Optional, Tuple


class Result:
    """Represents the grading result of a submission."""
    
    def __init__(
        self,
        result_id: str,
        submission_id: str,
        exam_id: str,
        student_id: str,
        score: float,
        total_questions: int,
        correct_answers: int,
        wrong_answers: int,
        graded_at: Optional[str] = None,
        details: Optional[List[dict]] = None
    ):
        self.result_id = result_id
        self.submission_id = submission_id
        self.exam_id = exam_id
        self.student_id = student_id
        self.score = score
        self.total_questions = total_questions
        self.correct_answers = correct_answers
        self.wrong_answers = wrong_answers
        self.graded_at = graded_at or datetime.utcnow().isoformat() + 'Z'
        self.details = details or []
    
    def validate(self) -> Tuple[bool, str]:
        """Validate result data.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.result_id:
            return False, "Mã kết quả không được để trống"
        
        if not self.submission_id:
            return False, "Mã bài làm không được để trống"
        
        if not self.exam_id:
            return False, "Mã đề thi không được để trống"
        
        if not self.student_id:
            return False, "Mã học sinh không được để trống"
        
        if self.score < 0 or self.score > 10:
            return False, "Điểm số phải nằm trong khoảng 0-10"
        
        if self.total_questions <= 0:
            return False, "Tổng số câu hỏi phải lớn hơn 0"
        
        if self.correct_answers < 0 or self.correct_answers > self.total_questions:
            return False, "Số câu đúng không hợp lệ"
        
        if self.wrong_answers < 0 or self.wrong_answers > self.total_questions:
            return False, "Số câu sai không hợp lệ"
        
        if self.correct_answers + self.wrong_answers != self.total_questions:
            return False, "Tổng số câu đúng và sai phải bằng tổng số câu hỏi"
        
        return True, ""
    
    def to_dict(self) -> dict:
        """Convert result to dictionary."""
        return {
            'result_id': self.result_id,
            'submission_id': self.submission_id,
            'exam_id': self.exam_id,
            'student_id': self.student_id,
            'score': self.score,
            'total_questions': self.total_questions,
            'correct_answers': self.correct_answers,
            'wrong_answers': self.wrong_answers,
            'graded_at': self.graded_at,
            'details': self.details
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Result':
        """Create result from dictionary."""
        return cls(
            result_id=data['result_id'],
            submission_id=data['submission_id'],
            exam_id=data['exam_id'],
            student_id=data['student_id'],
            score=data['score'],
            total_questions=data['total_questions'],
            correct_answers=data['correct_answers'],
            wrong_answers=data['wrong_answers'],
            graded_at=data.get('graded_at'),
            details=data.get('details', [])
        )
