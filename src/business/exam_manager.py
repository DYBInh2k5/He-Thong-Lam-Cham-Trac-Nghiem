"""Exam Manager - Business logic for exam management."""

from typing import List, Optional, Tuple
from datetime import datetime
import uuid

from src.models.exam import Exam, Question
from src.storage.file_storage import FileStorageManager


class ExamManager:
    """Manages exam-related business logic."""
    
    def __init__(self, storage: FileStorageManager):
        """Initialize ExamManager.
        
        Args:
            storage: FileStorageManager instance
        """
        self.storage = storage
    
    def create_exam(self, title: str, teacher_id: str) -> Tuple[bool, str, Optional[str]]:
        """Create a new exam.
        
        Args:
            title: Exam title
            teacher_id: ID of the teacher creating the exam
        
        Returns:
            Tuple of (success, message, exam_id)
        """
        if not title:
            return False, "Tên đề thi không được để trống", None
        
        if not teacher_id:
            return False, "Mã giáo viên không được để trống", None
        
        # Generate unique exam ID
        exam_id = f"E{uuid.uuid4().hex[:8].upper()}"
        
        # Create exam object
        exam = Exam(
            exam_id=exam_id,
            title=title,
            created_by=teacher_id,
            questions=[]
        )
        
        # Save to storage
        success = self.storage.save_exam(exam.to_dict())
        
        if success:
            return True, "Tạo đề thi thành công", exam_id
        else:
            return False, "Không thể lưu đề thi", None
    
    def add_question(
        self,
        exam_id: str,
        content: str,
        choices: dict,
        correct_answer: str
    ) -> Tuple[bool, str, Optional[str]]:
        """Add a question to an exam.
        
        Args:
            exam_id: ID of the exam
            content: Question content
            choices: Dictionary of choices {A, B, C, D}
            correct_answer: Correct answer (A, B, C, or D)
        
        Returns:
            Tuple of (success, message, question_id)
        """
        # Load exam
        exam_dict = self.storage.load_exam(exam_id)
        if not exam_dict:
            return False, f"Đề thi không tồn tại: {exam_id}", None
        
        exam = Exam.from_dict(exam_dict)
        
        # Generate question ID
        question_id = f"Q{len(exam.questions) + 1:03d}"
        
        # Create question
        question = Question(
            question_id=question_id,
            content=content,
            choices=choices,
            correct_answer=correct_answer
        )
        
        # Validate question
        is_valid, error_msg = question.validate()
        if not is_valid:
            return False, error_msg, None
        
        # Add question to exam
        success, msg = exam.add_question(question)
        if not success:
            return False, msg, None
        
        # Save exam
        if self.storage.save_exam(exam.to_dict()):
            return True, "Thêm câu hỏi thành công", question_id
        else:
            return False, "Không thể lưu đề thi", None
    
    def update_exam(self, exam_id: str, updates: dict) -> Tuple[bool, str]:
        """Update exam information.
        
        Args:
            exam_id: ID of the exam to update
            updates: Dictionary of fields to update
        
        Returns:
            Tuple of (success, message)
        """
        # Load exam
        exam_dict = self.storage.load_exam(exam_id)
        if not exam_dict:
            return False, f"Đề thi không tồn tại: {exam_id}"
        
        # Update allowed fields (not exam_id)
        if 'title' in updates:
            exam_dict['title'] = updates['title']
        
        if 'questions' in updates:
            exam_dict['questions'] = updates['questions']
        
        # Validate updated exam
        exam = Exam.from_dict(exam_dict)
        is_valid, error_msg = exam.validate()
        if not is_valid:
            return False, error_msg
        
        # Save updated exam
        if self.storage.save_exam(exam.to_dict()):
            return True, "Cập nhật đề thi thành công"
        else:
            return False, "Không thể lưu đề thi"
    
    def delete_exam(self, exam_id: str) -> Tuple[bool, str]:
        """Delete an exam.
        
        Args:
            exam_id: ID of the exam to delete
        
        Returns:
            Tuple of (success, message)
        """
        # Check if exam exists
        exam_dict = self.storage.load_exam(exam_id)
        if not exam_dict:
            return False, f"Đề thi không tồn tại: {exam_id}"
        
        # Delete exam
        if self.storage.delete_exam(exam_id):
            return True, "Xóa đề thi thành công"
        else:
            return False, "Không thể xóa đề thi"
    
    def get_exam(self, exam_id: str) -> Tuple[bool, str, Optional[dict]]:
        """Get an exam by ID.
        
        Args:
            exam_id: ID of the exam
        
        Returns:
            Tuple of (success, message, exam_dict)
        """
        exam_dict = self.storage.load_exam(exam_id)
        if exam_dict:
            return True, "Lấy đề thi thành công", exam_dict
        else:
            return False, f"Đề thi không tồn tại: {exam_id}", None
    
    def list_all_exams(self) -> Tuple[bool, str, List[dict]]:
        """List all exams.
        
        Returns:
            Tuple of (success, message, list of exam dicts)
        """
        exams = self.storage.list_exams()
        return True, f"Tìm thấy {len(exams)} đề thi", exams
    
    def validate_exam(self, exam_dict: dict) -> Tuple[bool, str]:
        """Validate an exam dictionary.
        
        Args:
            exam_dict: Exam dictionary to validate
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            exam = Exam.from_dict(exam_dict)
            return exam.validate()
        except Exception as e:
            return False, f"Lỗi khi validate đề thi: {str(e)}"
