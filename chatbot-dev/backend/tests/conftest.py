"""
Test configuration for the hybrid chatbot system
"""

import pytest
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Test configuration
TEST_DATABASE = "test_chatbot.db"
TEST_CACHE_DIR = "./test_cache"
TEST_DOCUMENTS_DIR = "./test_documents"

@pytest.fixture(scope="session")
def test_config():
    """Test configuration fixture"""
    return {
        "TESTING": True,
        "DATABASE": TEST_DATABASE,
        "CACHE_DIR": TEST_CACHE_DIR,
        "DOCUMENTS_DIR": TEST_DOCUMENTS_DIR,
        "GOOGLE_API_KEY": "test-api-key",
        "DEBUG": False
    }

@pytest.fixture(scope="function")
def clean_test_env():
    """Clean test environment before and after tests"""
    yield
    # Cleanup after test
    if os.path.exists(TEST_DATABASE):
        os.remove(TEST_DATABASE)
    if os.path.exists(TEST_CACHE_DIR):
        import shutil
        shutil.rmtree(TEST_CACHE_DIR)

@pytest.fixture
def mock_orchestrator():
    """Mock orchestrator for testing"""
    from unittest.mock import Mock
    orchestrator = Mock()
    orchestrator.process_hybrid_request.return_value = {
        "success": True,
        "response": "Test response",
        "metadata": {"flow_path": ["test"]}
    }
    return orchestrator
