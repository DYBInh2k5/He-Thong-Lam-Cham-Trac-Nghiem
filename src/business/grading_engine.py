"""Grading Engine - Chấm điểm tự động."""

from typing import Tuple, Optional
from datetime import datetime
import uuid

from src.storage.file_storage import FileStorageManager
from src.models.result import Result


class GradingEngine:
    """Chấm điểm tự động cho bài thi."""
    
    def __init__(self, storage: FileStorageManager):
        """Initialize GradingEngine.
        
        Args:
            storage: FileStorageManager instance
        """
        self.storage = storage
    
    def grade_submission(self, submission_id: str) -> Tuple[bool, str, Optional[dict]]:
        """Chấm điểm một bài làm.
        
        Args:
            submission_id: ID của bài làm
        
        Returns:
            Tuple of (success, message, result_dict)
        """
        # Load submission
        submission_dict = self.storage.load_submission(submission_id)
        if not submission_dict:
            return False, f"Bài làm không tồn tại: {submission_id}", None
        
        # Load exam
        exam_dict = self.storage.load_exam(submission_dict['exam_id'])
        if not exam_dict:
            return False, f"Đề thi không tồn tại: {submission_dict['exam_id']}", None
        
        # Grade each question
        total_questions = len(exam_dict['questions'])
        correct_answers = 0
        details = []
        
        for question in exam_dict['questions']:
            question_id = question['question_id']
            correct_answer = question['correct_answer']
            student_answer = submission_dict['answers'].get(question_id, '')
            
            is_correct = self.compare_answers(student_answer, correct_answer)
            if is_correct:
                correct_answers += 1
            
            details.append({
                'question_id': question_id,
                'student_answer': student_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct
            })
        
        # Calculate score
        wrong_answers = total_questions - correct_answers
        score = self.calculate_score(correct_answers, total_questions)
        
        # Create result
        result_id = f"R{uuid.uuid4().hex[:8].upper()}"
        result = Result(
            result_id=result_id,
            submission_id=submission_id,
            exam_id=submission_dict['exam_id'],
            student_id=submission_dict['student_id'],
            score=score,
            total_questions=total_questions,
            correct_answers=correct_answers,
            wrong_answers=wrong_answers,
            details=details
        )
        
        # Validate and save
        is_valid, error_msg = result.validate()
        if not is_valid:
            return False, error_msg, None
        
        result_dict = result.to_dict()
        if self.storage.save_result(result_dict):
            return True, "Chấm bài thành công", result_dict
        else:
            return False, "Không thể lưu kết quả", None
    
    def calculate_score(self, correct: int, total: int) -> float:
        """Tính điểm theo thang 10.
        
        Args:
            correct: Số câu đúng
            total: Tổng số câu
        
        Returns:
            Điểm (0-10)
        """
        if total == 0:
            return 0.0
        return round((correct / total) * 10, 2)
    
    def compare_answers(self, student_answer: str, correct_answer: str) -> bool:
        """So sánh câu trả lời.
        
        Args:
            student_answer: Đáp án của học sinh
            correct_answer: Đáp án đúng
        
        Returns:
            True nếu đúng
        """
        return student_answer.strip().upper() == correct_answer.strip().upper()
    
    def get_result(self, result_id: str) -> Tuple[bool, str, Optional[dict]]:
        """Lấy kết quả chấm bài.
        
        Args:
            result_id: ID của kết quả
        
        Returns:
            Tuple of (success, message, result_dict)
        """
        result_dict = self.storage.load_result(result_id)
        if result_dict:
            return True, "Lấy kết quả thành công", result_dict
        else:
            return False, f"Kết quả không tồn tại: {result_id}", None
