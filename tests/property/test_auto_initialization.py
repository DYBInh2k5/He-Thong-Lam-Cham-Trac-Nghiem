"""Property-based tests for auto-initialization.

Feature: multiple-choice-grading-system, Property 26: Auto-initialization
"""

import tempfile
import shutil
import os
from hypothesis import given, strategies as st, settings
from src.storage.file_storage import FileStorageManager


@given(st.text(min_size=1, max_size=20, alphabet=st.characters(
    whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=48, max_codepoint=122
)))
@settings(max_examples=100)
def test_auto_initialization_creates_directories(base_dir_name):
    """
    Feature: multiple-choice-grading-system, Property 26: Auto-initialization
    
    For any missing data file, the first access should automatically create 
    the file with valid default structure.
    
    Validates: Requirements 10.5
    """
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Create a non-existent subdirectory path
        base_path = os.path.join(temp_dir, base_dir_name)
        
        # Verify directory doesn't exist yet
        assert not os.path.exists(base_path), "Directory should not exist yet"
        
        # Initialize storage manager - should create directories
        storage = FileStorageManager(base_path=base_path)
        
        # Verify base directory was created
        assert os.path.exists(base_path), "Base directory should be created"
        
        # Verify all required subdirectories were created
        required_dirs = ['exams', 'submissions', 'results', 'users']
        for dir_name in required_dirs:
            dir_path = os.path.join(base_path, dir_name)
            assert os.path.exists(dir_path), f"Directory '{dir_name}' should be created"
            assert os.path.isdir(dir_path), f"'{dir_name}' should be a directory"
    
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)


@given(st.text(min_size=1, max_size=20, alphabet=st.characters(
    whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=48, max_codepoint=122
)))
@settings(max_examples=100)
def test_load_nonexistent_file_returns_none(entity_id):
    """Test that loading a non-existent file returns None gracefully."""
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Initialize storage manager
        storage = FileStorageManager(base_path=temp_dir)
        
        # Try to load non-existent entities - should return None, not crash
        exam = storage.load_exam(entity_id)
        assert exam is None, "Loading non-existent exam should return None"
        
        submission = storage.load_submission(entity_id)
        assert submission is None, "Loading non-existent submission should return None"
        
        result = storage.load_result(entity_id)
        assert result is None, "Loading non-existent result should return None"
        
        user = storage.load_user(entity_id)
        assert user is None, "Loading non-existent user should return None"
    
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)
