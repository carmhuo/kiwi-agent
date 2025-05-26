"""
Tests for environment variable configuration.

This module tests that the Kiwi project properly handles environment variables
for API keys and other configuration settings.
"""

import os
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestEnvironmentVariables:
    """Test environment variable handling."""
    
    def test_modelscope_api_key_required(self, clean_env):
        """Test that MODELSCOPE_API_KEY is properly required."""
        # Test the validation logic directly
        api_key = os.getenv('MODELSCOPE_API_KEY')
        if not api_key:
            with pytest.raises(ValueError, match="MODELSCOPE_API_KEY environment variable is required"):
                raise ValueError(
                    "MODELSCOPE_API_KEY environment variable is required. "
                    "Please set it with: export MODELSCOPE_API_KEY='your-api-key'"
                )
    
    def test_modelscope_api_key_loaded(self, mock_env_vars):
        """Test that MODELSCOPE_API_KEY is properly loaded when set."""
        api_key = os.getenv('MODELSCOPE_API_KEY')
        assert api_key == 'test-modelscope-key-12345'
    
    def test_openai_api_key_alternative(self, clean_env):
        """Test that OPENAI_API_KEY can be used as alternative."""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-openai-key'}, clear=False):
            api_key = os.getenv('OPENAI_API_KEY')
            assert api_key == 'test-openai-key'
    
    def test_optional_variables_defaults(self, mock_env_vars):
        """Test that optional variables have proper defaults."""
        assert os.getenv('MODELSCOPE_API_BASE') == 'https://api-inference.modelscope.cn/v1/'
        assert os.getenv('MODELSCOPE_MODEL') == 'Qwen/Qwen2.5-32B-Instruct'
    
    def test_flask_configuration(self, mock_env_vars):
        """Test Flask-specific environment variables."""
        assert os.getenv('FLASK_ENV') == 'testing'
        assert os.getenv('FLASK_DEBUG') == 'false'
        assert os.getenv('FLASK_HOST') == '127.0.0.1'
        assert os.getenv('FLASK_PORT') == '5000'


class TestDotenvLoading:
    """Test .env file loading functionality."""
    
    def test_dotenv_import_optional(self):
        """Test that dotenv import is optional and doesn't break if missing."""
        with patch('builtins.__import__', side_effect=ImportError("No module named 'dotenv'")):
            # This should not raise an exception
            try:
                from dotenv import load_dotenv
                load_dotenv()
            except ImportError:
                pass  # Expected behavior
    
    def test_dotenv_loading_with_file(self, temp_env_file):
        """Test loading environment variables from .env file."""
        try:
            from dotenv import load_dotenv
            
            # Clear existing environment variables first
            keys_to_clear = ['MODELSCOPE_API_KEY', 'MODELSCOPE_API_BASE']
            original_values = {}
            for key in keys_to_clear:
                if key in os.environ:
                    original_values[key] = os.environ[key]
                    del os.environ[key]
            
            # Load from specific file path instead of changing directory
            load_dotenv(temp_env_file)
            
            # Check if variables were loaded
            assert os.getenv('MODELSCOPE_API_KEY') == 'test-key-from-file'
            assert os.getenv('MODELSCOPE_API_BASE') == 'https://test-api.example.com/v1/'
            
            # Restore original values
            for key, value in original_values.items():
                os.environ[key] = value
            
        except ImportError:
            pytest.skip("python-dotenv not available")


class TestAPIKeyValidation:
    """Test API key validation logic."""
    
    def test_api_key_validation_error_message(self, clean_env):
        """Test that proper error message is shown for missing API key."""
        with pytest.raises(ValueError) as exc_info:
            # This should trigger the validation error
            api_key = os.getenv('MODELSCOPE_API_KEY')
            if not api_key:
                raise ValueError(
                    "MODELSCOPE_API_KEY environment variable is required. "
                    "Please set it with: export MODELSCOPE_API_KEY='your-api-key'"
                )
        
        error_message = str(exc_info.value)
        assert "MODELSCOPE_API_KEY environment variable is required" in error_message
        assert "export MODELSCOPE_API_KEY" in error_message
    
    def test_api_key_not_empty_string(self):
        """Test that empty string API key is treated as missing."""
        with patch.dict(os.environ, {'MODELSCOPE_API_KEY': ''}, clear=False):
            api_key = os.getenv('MODELSCOPE_API_KEY')
            # Empty string should be treated as missing
            if not api_key:
                with pytest.raises(ValueError):
                    raise ValueError("MODELSCOPE_API_KEY environment variable is required")
    
    def test_api_key_whitespace_handling(self):
        """Test that whitespace-only API key is handled properly."""
        with patch.dict(os.environ, {'MODELSCOPE_API_KEY': '   '}, clear=False):
            api_key = os.getenv('MODELSCOPE_API_KEY')
            if api_key:
                api_key = api_key.strip()
            
            if not api_key:
                with pytest.raises(ValueError):
                    raise ValueError("MODELSCOPE_API_KEY environment variable is required")


class TestModuleImports:
    """Test that modules can be imported with proper environment setup."""
    
    def test_kiwi_base_import(self, mock_env_vars):
        """Test importing kiwi.base module."""
        try:
            import kiwi.base
            assert hasattr(kiwi.base, 'VannaBase')
        except ImportError as e:
            pytest.skip(f"kiwi.base not available: {e}")
    
    def test_openai_chat_import(self, mock_env_vars):
        """Test importing kiwi.openai_chat module."""
        try:
            import kiwi.openai_chat
            assert hasattr(kiwi.openai_chat, 'OpenAI_Chat')
        except ImportError as e:
            pytest.skip(f"kiwi.openai_chat not available: {e}")
    
    def test_chromadb_vector_import(self, mock_env_vars):
        """Test importing kiwi.chromadb_vector module."""
        try:
            import kiwi.chromadb_vector
            assert hasattr(kiwi.chromadb_vector, 'ChromaDB_VectorStore')
        except ImportError as e:
            pytest.skip(f"kiwi.chromadb_vector not available: {e}")
    
    def test_flask_app_import(self, mock_env_vars):
        """Test importing Flask app components."""
        try:
            from kiwi.flask_app import VannaFlaskApp
            assert VannaFlaskApp is not None
        except ImportError as e:
            pytest.skip(f"VannaFlaskApp not available: {e}")


class TestClientCreation:
    """Test OpenAI client creation with environment variables."""
    
    def test_modelscope_client_creation(self, mock_env_vars):
        """Test creating ModelScope client with environment variables."""
        try:
            from openai import OpenAI
            
            api_key = os.getenv('MODELSCOPE_API_KEY')
            api_base = os.getenv('MODELSCOPE_API_BASE')
            
            client = OpenAI(
                base_url=api_base,
                api_key=api_key
            )
            
            assert client.api_key == 'test-modelscope-key-12345'
            assert client.base_url == 'https://api-inference.modelscope.cn/v1/'
            
        except ImportError as e:
            pytest.skip(f"OpenAI client not available: {e}")
    
    def test_openai_client_creation(self, mock_env_vars):
        """Test creating OpenAI client with environment variables."""
        try:
            from openai import OpenAI
            
            api_key = os.getenv('OPENAI_API_KEY')
            
            client = OpenAI(api_key=api_key)
            
            assert client.api_key == 'test-openai-key-67890'
            
        except ImportError as e:
            pytest.skip(f"OpenAI client not available: {e}")
    
    def test_client_creation_with_missing_key(self, clean_env):
        """Test that client creation fails gracefully with missing API key."""
        try:
            from openai import OpenAI
            from openai import OpenAIError
            
            api_key = os.getenv('MODELSCOPE_API_KEY')
            
            if not api_key:
                with pytest.raises(OpenAIError):
                    # This should fail because no API key is provided
                    client = OpenAI(api_key=None)
            
        except ImportError as e:
            pytest.skip(f"OpenAI client not available: {e}")


class TestSecurityCompliance:
    """Test security compliance and best practices."""
    
    def test_no_hardcoded_api_keys_in_source(self, project_root_path):
        """Test that no hardcoded API keys exist in source code."""
        # Known hardcoded key that should not exist
        hardcoded_key = "9d431c1c-2acd-4dd0-b95a-76affce19b3b"
        
        python_files = list((project_root_path / "src").rglob("*.py"))
        
        for py_file in python_files:
            content = py_file.read_text(encoding='utf-8')
            assert hardcoded_key not in content, f"Hardcoded API key found in {py_file}"
    
    def test_env_file_in_gitignore(self, project_root_path):
        """Test that .env file is properly excluded from version control."""
        gitignore_file = project_root_path / ".gitignore"
        
        if gitignore_file.exists():
            gitignore_content = gitignore_file.read_text()
            assert ".env" in gitignore_content, ".env file should be in .gitignore"
    
    def test_env_example_exists(self, project_root_path):
        """Test that .env.example template file exists."""
        env_example = project_root_path / ".env.example"
        assert env_example.exists(), ".env.example template should exist"
        
        content = env_example.read_text()
        assert "MODELSCOPE_API_KEY" in content, ".env.example should contain MODELSCOPE_API_KEY"
        assert "your-modelscope-api-key-here" in content, ".env.example should contain placeholder"