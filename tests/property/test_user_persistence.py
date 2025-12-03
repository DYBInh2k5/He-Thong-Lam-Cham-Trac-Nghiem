"""Property-based tests for user persistence.

Feature: multiple-choice-grading-system, Property 14: User persistence round-trip
"""

import tempfile
import shutil
from hypothesis import given, strategies as st, settings
from src.models.user import User
from src.storage.file_storage import FileStorageManager


# Strategy for generating valid users
@st.composite
def user_strategy(draw):
    """Generate a valid user."""
    user_id = draw(st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=48, max_codepoint=122
    )))
    name = draw(st.text(min_size=1, max_size=100))
    role = draw(st.sampled_from(['teacher', 'student']))
    
    return User(
        user_id=user_id,
        name=name,
        role=role
    )


@given(user_strategy())
@settings(max_examples=100)
def test_user_persistence_round_trip(user):
    """
    Feature: multiple-choice-grading-system, Property 14: User persistence round-trip
    
    For any valid user with name, user_id, and role, saving then loading should 
    produce an equivalent user with all information preserved.
    
    Validates: Requirements 5.1
    """
    # Create temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Initialize storage manager
        storage = FileStorageManager(base_path=temp_dir)
        
        # Convert user to dict and save
        user_dict = user.to_dict()
        success = storage.save_user(user_dict)
        assert success, "Failed to save user"
        
        # Load user back
        loaded_dict = storage.load_user(user.user_id)
        assert loaded_dict is not None, "Failed to load user"
        
        # Convert back to User object
        loaded_user = User.from_dict(loaded_dict)
        
        # Verify all fields are preserved
        assert loaded_user.user_id == user.user_id, "User ID not preserved"
        assert loaded_user.name == user.name, "Name not preserved"
        assert loaded_user.role == user.role, "Role not preserved"
    
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)
