"""User data model."""

from datetime import datetime
from typing import Optional, Tuple


class User:
    """Represents a user (teacher or student) in the system."""
    
    def __init__(
        self,
        user_id: str,
        name: str,
        role: str,
        created_at: Optional[str] = None
    ):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.created_at = created_at or datetime.utcnow().isoformat() + 'Z'
    
    def validate(self) -> Tuple[bool, str]:
        """Validate user data.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.user_id:
            return False, "Mã người dùng không được để trống"
        
        if not self.name:
            return False, "Tên người dùng không được để trống"
        
        if self.role not in {'teacher', 'student'}:
            return False, "Vai trò phải là 'teacher' hoặc 'student'"
        
        return True, ""
    
    def to_dict(self) -> dict:
        """Convert user to dictionary."""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'role': self.role,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create user from dictionary."""
        return cls(
            user_id=data['user_id'],
            name=data['name'],
            role=data['role'],
            created_at=data.get('created_at')
        )
