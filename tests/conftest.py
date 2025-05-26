"""
Pytest configuration and shared fixtures for Kiwi tests.
"""

import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch

# Add src directory to Python path for imports
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def mock_env_vars():
    """Fixture that provides mock environment variables for testing."""
    mock_vars = {
        'MODELSCOPE_API_KEY': 'test-modelscope-key-12345',
        'OPENAI_API_KEY': 'test-openai-key-67890',
        'MODELSCOPE_API_BASE': 'https://api-inference.modelscope.cn/v1/',
        'MODELSCOPE_MODEL': 'Qwen/Qwen2.5-32B-Instruct',
        'FLASK_ENV': 'testing',
        'FLASK_DEBUG': 'false',
        'FLASK_HOST': '127.0.0.1',
        'FLASK_PORT': '5000'
    }
    
    with patch.dict(os.environ, mock_vars, clear=False):
        yield mock_vars


@pytest.fixture
def clean_env():
    """Fixture that provides a clean environment without API keys."""
    keys_to_remove = [
        'MODELSCOPE_API_KEY',
        'OPENAI_API_KEY',
        'MODELSCOPE_API_BASE',
        'MODELSCOPE_MODEL'
    ]
    
    original_values = {}
    for key in keys_to_remove:
        if key in os.environ:
            original_values[key] = os.environ[key]
            del os.environ[key]
    
    yield
    
    # Restore original values
    for key, value in original_values.items():
        os.environ[key] = value


@pytest.fixture
def project_root_path():
    """Fixture that provides the project root path."""
    return Path(__file__).parent.parent


@pytest.fixture
def temp_env_file(tmp_path):
    """Fixture that creates a temporary .env file for testing."""
    env_content = """# Test environment file
MODELSCOPE_API_KEY=test-key-from-file
MODELSCOPE_API_BASE=https://test-api.example.com/v1/
MODELSCOPE_MODEL=test-model
FLASK_ENV=testing
"""
    env_file = tmp_path / ".env"
    env_file.write_text(env_content)
    return env_file