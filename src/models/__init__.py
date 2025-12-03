"""Data models for the multiple-choice grading system."""

from .exam import Exam, Question
from .submission import Submission
from .result import Result
from .user import User

__all__ = ['Exam', 'Question', 'Submission', 'Result', 'User']
