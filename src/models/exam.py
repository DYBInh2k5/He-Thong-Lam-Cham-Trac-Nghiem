"""Exam and Question data models."""

from datetime import datetime
from typing import Dict, List, Optional, Tuple


class Question:
    """Represents a multiple-choice question."""
    
    def __init__(
        self,
        question_id: str,
        content: str,
        choices: Dict[str, str],
        correct_answer: str
    ):
        self.question_id = question_id
        self.content = content
        self.choices = choices
        self.correct_answer = correct_answer
    
    def validate(self) -> Tuple[bool, str]:
        """Validate question data.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.question_id:
            return False, "Mã câu hỏi không được để trống"
        
        if not self.content:
            return False, "Nội dung câu hỏi không được để trống"
        
        # Check if all choices A, B, C, D are present
        required_choices = {'A', 'B', 'C', 'D'}
        if set(self.choices.keys()) != required_choices:
            return False, "Câu hỏi phải có đầy đủ 4 lựa chọn A, B, C, D"
        
        # Check if all choices have content
        for choice, text in self.choices.items():
            if not text:
                return False, f"Lựa chọn {choice} không được để trống"
        
        # Check if correct answer is valid
        if self.correct_answer not in required_choices:
            return False, "Đáp án đúng phải là A, B, C hoặc D"
        
        return True, ""
    
    def to_dict(self) -> dict:
        """Convert question to dictionary."""
        return {
            'question_id': self.question_id,
            'content': self.content,
            'choices': self.choices,
            'correct_answer': self.correct_answer
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Question':
        """Create question from dictionary."""
        return cls(
            question_id=data['question_id'],
            content=data['content'],
            choices=data['choices'],
            correct_answer=data['correct_answer']
        )


class Exam:
    """Represents an exam with multiple questions."""
    
    def __init__(
        self,
        exam_id: str,
        title: str,
        created_by: str,
        created_at: Optional[str] = None,
        questions: Optional[List[Question]] = None
    ):
        self.exam_id = exam_id
        self.title = title
        self.created_by = created_by
        self.created_at = created_at or datetime.utcnow().isoformat() + 'Z'
        self.questions = questions or []
    
    def add_question(self, question: Question) -> Tuple[bool, str]:
        """Add a question to the exam.
        
        Returns:
            Tuple of (success, message)
        """
        # Validate question first
        is_valid, error_msg = question.validate()
        if not is_valid:
            return False, error_msg
        
        # Check for duplicate question_id
        if any(q.question_id == question.question_id for q in self.questions):
            return False, f"Câu hỏi với mã {question.question_id} đã tồn tại"
        
        self.questions.append(question)
        return True, "Thêm câu hỏi thành công"
    
    def validate(self) -> Tuple[bool, str]:
        """Validate exam data.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.exam_id:
            return False, "Mã đề thi không được để trống"
        
        if not self.title:
            return False, "Tên đề thi không được để trống"
        
        if not self.created_by:
            return False, "Mã giáo viên không được để trống"
        
        if len(self.questions) == 0:
            return False, "Đề thi phải có ít nhất một câu hỏi"
        
        # Validate all questions
        for question in self.questions:
            is_valid, error_msg = question.validate()
            if not is_valid:
                return False, f"Câu hỏi {question.question_id}: {error_msg}"
        
        return True, ""
    
    def to_dict(self) -> dict:
        """Convert exam to dictionary."""
        return {
            'exam_id': self.exam_id,
            'title': self.title,
            'created_by': self.created_by,
            'created_at': self.created_at,
            'questions': [q.to_dict() for q in self.questions]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Exam':
        """Create exam from dictionary."""
        questions = [Question.from_dict(q) for q in data.get('questions', [])]
        return cls(
            exam_id=data['exam_id'],
            title=data['title'],
            created_by=data['created_by'],
            created_at=data.get('created_at'),
            questions=questions
        )
