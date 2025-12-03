"""File storage manager for JSON-based persistence."""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional


class FileStorageManager:
    """Manages file-based storage for all entities."""
    
    def __init__(self, base_path: str = "data"):
        """Initialize storage manager.
        
        Args:
            base_path: Base directory for data storage
        """
        self.base_path = Path(base_path)
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        directories = ['exams', 'submissions', 'results', 'users']
        for dir_name in directories:
            dir_path = self.base_path / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def save_exam(self, exam: dict) -> bool:
        """Save an exam to file.
        
        Args:
            exam: Exam dictionary
        
        Returns:
            True if successful
        """
        try:
            exam_id = exam['exam_id']
            file_path = self.base_path / 'exams' / f'{exam_id}.json'
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(exam, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def load_exam(self, exam_id: str) -> Optional[dict]:
        """Load an exam from file.
        
        Args:
            exam_id: ID of the exam to load
        
        Returns:
            Exam dictionary or None if not found
        """
        try:
            file_path = self.base_path / 'exams' / f'{exam_id}.json'
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except Exception:
            return None
    
    def list_exams(self) -> List[dict]:
        """List all exams.
        
        Returns:
            List of exam dictionaries
        """
        exams = []
        exams_dir = self.base_path / 'exams'
        if not exams_dir.exists():
            return exams
        
        for file_path in exams_dir.glob('*.json'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    exams.append(json.load(f))
            except Exception:
                continue
        
        return exams
    
    def delete_exam(self, exam_id: str) -> bool:
        """Delete an exam file.
        
        Args:
            exam_id: ID of the exam to delete
        
        Returns:
            True if successful
        """
        try:
            file_path = self.base_path / 'exams' / f'{exam_id}.json'
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception:
            return False
    
    def save_submission(self, submission: dict) -> bool:
        """Save a submission to file."""
        try:
            submission_id = submission['submission_id']
            file_path = self.base_path / 'submissions' / f'{submission_id}.json'
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(submission, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def load_submission(self, submission_id: str) -> Optional[dict]:
        """Load a submission from file."""
        try:
            file_path = self.base_path / 'submissions' / f'{submission_id}.json'
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except Exception:
            return None
    
    def save_result(self, result: dict) -> bool:
        """Save a result to file."""
        try:
            result_id = result['result_id']
            file_path = self.base_path / 'results' / f'{result_id}.json'
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def load_result(self, result_id: str) -> Optional[dict]:
        """Load a result from file."""
        try:
            file_path = self.base_path / 'results' / f'{result_id}.json'
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except Exception:
            return None
    
    def save_user(self, user: dict) -> bool:
        """Save a user to file."""
        try:
            user_id = user['user_id']
            file_path = self.base_path / 'users' / f'{user_id}.json'
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(user, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def load_user(self, user_id: str) -> Optional[dict]:
        """Load a user from file."""
        try:
            file_path = self.base_path / 'users' / f'{user_id}.json'
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except Exception:
            return None
    
    def list_users(self, role: Optional[str] = None) -> List[dict]:
        """List all users, optionally filtered by role.
        
        Args:
            role: Optional role filter ('teacher' or 'student')
        
        Returns:
            List of user dictionaries
        """
        users = []
        users_dir = self.base_path / 'users'
        if not users_dir.exists():
            return users
        
        for file_path in users_dir.glob('*.json'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    user = json.load(f)
                    if role is None or user.get('role') == role:
                        users.append(user)
            except Exception:
                continue
        
        return users
    
    def delete_user(self, user_id: str) -> bool:
        """Delete a user file.
        
        Args:
            user_id: ID of the user to delete
        
        Returns:
            True if successful
        """
        try:
            file_path = self.base_path / 'users' / f'{user_id}.json'
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception:
            return False
    
    def list_submissions(self, exam_id: Optional[str] = None, student_id: Optional[str] = None) -> List[dict]:
        """List submissions, optionally filtered by exam_id or student_id.
        
        Args:
            exam_id: Optional exam ID filter
            student_id: Optional student ID filter
        
        Returns:
            List of submission dictionaries
        """
        submissions = []
        submissions_dir = self.base_path / 'submissions'
        if not submissions_dir.exists():
            return submissions
        
        for file_path in submissions_dir.glob('*.json'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    submission = json.load(f)
                    # Apply filters
                    if exam_id and submission.get('exam_id') != exam_id:
                        continue
                    if student_id and submission.get('student_id') != student_id:
                        continue
                    submissions.append(submission)
            except Exception:
                continue
        
        return submissions
    
    def list_results(self, exam_id: Optional[str] = None, student_id: Optional[str] = None) -> List[dict]:
        """List results, optionally filtered by exam_id or student_id.
        
        Args:
            exam_id: Optional exam ID filter
            student_id: Optional student ID filter
        
        Returns:
            List of result dictionaries
        """
        results = []
        results_dir = self.base_path / 'results'
        if not results_dir.exists():
            return results
        
        for file_path in results_dir.glob('*.json'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    result = json.load(f)
                    # Apply filters
                    if exam_id and result.get('exam_id') != exam_id:
                        continue
                    if student_id and result.get('student_id') != student_id:
                        continue
                    results.append(result)
            except Exception:
                continue
        
        return results
    
    def import_from_json(self, file_path: str, data_type: str) -> bool:
        """Import data from a JSON file.
        
        Args:
            file_path: Path to the JSON file
            data_type: Type of data ('exam', 'user', 'submission', 'result')
        
        Returns:
            True if successful
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Save based on data type
            if data_type == 'exam':
                return self.save_exam(data)
            elif data_type == 'user':
                return self.save_user(data)
            elif data_type == 'submission':
                return self.save_submission(data)
            elif data_type == 'result':
                return self.save_result(data)
            else:
                return False
        except Exception:
            return False
    
    def export_to_json(self, data: dict, file_path: str) -> bool:
        """Export data to a JSON file.
        
        Args:
            data: Data dictionary to export
            file_path: Path where to save the JSON file
        
        Returns:
            True if successful
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def import_from_csv(self, file_path: str) -> Optional[dict]:
        """Import exam questions from a CSV file.
        
        CSV format: question_id,content,choice_A,choice_B,choice_C,choice_D,correct_answer
        
        Args:
            file_path: Path to the CSV file
        
        Returns:
            Dictionary with questions list or None if failed
        """
        try:
            import csv
            questions = []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    question = {
                        'question_id': row['question_id'],
                        'content': row['content'],
                        'choices': {
                            'A': row['choice_A'],
                            'B': row['choice_B'],
                            'C': row['choice_C'],
                            'D': row['choice_D']
                        },
                        'correct_answer': row['correct_answer']
                    }
                    questions.append(question)
            
            return {'questions': questions}
        except Exception:
            return None
    
    def export_to_csv(self, data: List[dict], file_path: str) -> bool:
        """Export data to a CSV file.
        
        Args:
            data: List of dictionaries to export
            file_path: Path where to save the CSV file
        
        Returns:
            True if successful
        """
        try:
            import csv
            
            if not data:
                return False
            
            # Get all keys from first item
            fieldnames = list(data[0].keys())
            
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            return True
        except Exception:
            return False
