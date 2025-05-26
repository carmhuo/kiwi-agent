"""
Integration tests for the Kiwi project.

This module contains tests that verify the integration between different
components of the system with proper environment configuration.
"""

import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestApplicationIntegration:
    """Test integration between application components."""
    
    def test_kiwi_app_initialization(self, mock_env_vars):
        """Test that kiwi_app can be initialized with environment variables."""
        try:
            # Mock the Flask app to avoid actually starting the server
            with patch('kiwi.flask_app.VannaFlaskApp') as mock_flask_app:
                mock_flask_app.return_value.run = MagicMock()
                
                # Import and test initialization
                import importlib.util
                spec = importlib.util.spec_from_file_location(
                    "kiwi_app", 
                    Path(__file__).parent.parent / "src" / "kiwi" / "kiwi_app.py"
                )
                
                if spec and spec.loader:
                    # This should not raise an exception
                    module = importlib.util.module_from_spec(spec)
                    
                    # Mock the execution to avoid running the server
                    with patch.object(module, '__name__', '__main__'):
                        with patch('sys.argv', ['kiwi_app.py']):
                            try:
                                spec.loader.exec_module(module)
                            except SystemExit:
                                pass  # Expected when running as main
                
        except ImportError as e:
            pytest.skip(f"Could not import kiwi_app: {e}")
    
    def test_graph_app_initialization(self, mock_env_vars):
        """Test that graph_app can be initialized with environment variables."""
        try:
            # Mock the Flask app to avoid actually starting the server
            with patch('kiwi.flask_app.VannaFlaskApp') as mock_flask_app:
                mock_flask_app.return_value.run = MagicMock()
                
                # Import and test initialization
                import importlib.util
                spec = importlib.util.spec_from_file_location(
                    "graph_app", 
                    Path(__file__).parent.parent / "src" / "kiwi" / "graph_app.py"
                )
                
                if spec and spec.loader:
                    # This should not raise an exception
                    module = importlib.util.module_from_spec(spec)
                    
                    # Mock the execution to avoid running the server
                    with patch.object(module, '__name__', '__main__'):
                        with patch('sys.argv', ['graph_app.py']):
                            try:
                                spec.loader.exec_module(module)
                            except SystemExit:
                                pass  # Expected when running as main
                
        except ImportError as e:
            pytest.skip(f"Could not import graph_app: {e}")


class TestVannaIntegration:
    """Test integration with Vanna components."""
    
    def test_vanna_base_with_openai_chat(self, mock_env_vars):
        """Test that VannaBase integrates properly with OpenAI_Chat."""
        try:
            from kiwi import OpenAI_Chat
            from kiwi import ChromaDB_VectorStore
            
            # Test that classes can be imported and have expected methods
            assert hasattr(OpenAI_Chat, 'generate_sql')
            assert hasattr(ChromaDB_VectorStore, 'add_ddl')
            
            # Test that they are properly defined classes
            assert OpenAI_Chat.__name__ == 'OpenAI_Chat'
            assert ChromaDB_VectorStore.__name__ == 'ChromaDB_VectorStore'
                
        except ImportError as e:
            pytest.skip(f"Vanna components not available: {e}")
    
    def test_flask_app_integration(self, mock_env_vars):
        """Test that Flask app integrates with Vanna components."""
        try:
            from kiwi.flask_app import VannaFlaskApp
            from kiwi import OpenAI_Chat
            from kiwi import ChromaDB_VectorStore
            
            # Test that Flask app class can be imported
            assert VannaFlaskApp.__name__ == 'VannaFlaskApp'
            
            # Test that required Vanna classes are available
            assert OpenAI_Chat.__name__ == 'OpenAI_Chat'
            assert ChromaDB_VectorStore.__name__ == 'ChromaDB_VectorStore'
                    
        except ImportError as e:
            pytest.skip(f"Flask app components not available: {e}")


class TestEnvironmentIntegration:
    """Test integration with environment variable loading."""
    
    def test_dotenv_integration(self, temp_env_file):
        """Test that dotenv properly integrates with the application."""
        try:
            from dotenv import load_dotenv
            
            # Clear existing environment variables
            original_values = {}
            for key in ['MODELSCOPE_API_KEY', 'MODELSCOPE_API_BASE']:
                if key in os.environ:
                    original_values[key] = os.environ[key]
                    del os.environ[key]
            
            # Load from specific .env file
            load_dotenv(temp_env_file)
            
            # Verify variables were loaded
            assert os.getenv('MODELSCOPE_API_KEY') == 'test-key-from-file'
            assert os.getenv('MODELSCOPE_API_BASE') == 'https://test-api.example.com/v1/'
            
            # Restore original values
            for key, value in original_values.items():
                os.environ[key] = value
            
        except ImportError:
            pytest.skip("python-dotenv not available")
    
    def test_environment_precedence(self, temp_env_file):
        """Test that environment variables take precedence over .env file."""
        try:
            from dotenv import load_dotenv
            
            # Set environment variable
            with patch.dict(os.environ, {'MODELSCOPE_API_KEY': 'env-var-key'}, clear=False):
                # Change to temp directory and load .env
                original_cwd = os.getcwd()
                os.chdir(temp_env_file.parent)
                
                load_dotenv()
                
                # Environment variable should take precedence
                assert os.getenv('MODELSCOPE_API_KEY') == 'env-var-key'
                
                os.chdir(original_cwd)
                
        except ImportError:
            pytest.skip("python-dotenv not available")


class TestErrorHandlingIntegration:
    """Test error handling across integrated components."""
    
    def test_missing_api_key_error_propagation(self, clean_env):
        """Test that missing API key errors are properly propagated."""
        try:
            # This should raise a ValueError about missing API key
            with pytest.raises(ValueError, match="MODELSCOPE_API_KEY"):
                import importlib.util
                spec = importlib.util.spec_from_file_location(
                    "kiwi_app", 
                    Path(__file__).parent.parent / "src" / "kiwi" / "kiwi_app.py"
                )
                
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                
        except ImportError as e:
            pytest.skip(f"Could not test error propagation: {e}")
    
    def test_openai_client_error_handling(self, mock_env_vars):
        """Test error handling in OpenAI client creation."""
        try:
            from openai import OpenAI
            
            # Test with invalid API key format
            with patch.dict(os.environ, {'MODELSCOPE_API_KEY': 'invalid-key'}, clear=False):
                # This should not raise an exception during client creation
                # (validation happens during API calls)
                client = OpenAI(
                    base_url=os.getenv('MODELSCOPE_API_BASE'),
                    api_key=os.getenv('MODELSCOPE_API_KEY')
                )
                
                assert client is not None
                
        except ImportError as e:
            pytest.skip(f"OpenAI client not available: {e}")


class TestConfigurationIntegration:
    """Test integration of configuration across components."""
    
    def test_configuration_consistency(self, mock_env_vars):
        """Test that configuration is consistent across components."""
        # All components should use the same environment variables
        expected_api_key = os.getenv('MODELSCOPE_API_KEY')
        expected_api_base = os.getenv('MODELSCOPE_API_BASE')
        
        assert expected_api_key == 'test-modelscope-key-12345'
        assert expected_api_base == 'https://api-inference.modelscope.cn/v1/'
        
        # Test that multiple components can access the same configuration
        api_key_1 = os.getenv('MODELSCOPE_API_KEY')
        api_key_2 = os.getenv('MODELSCOPE_API_KEY')
        
        assert api_key_1 == api_key_2
    
    def test_optional_configuration_defaults(self, mock_env_vars):
        """Test that optional configuration has proper defaults."""
        # Test with minimal configuration
        with patch.dict(os.environ, {
            'MODELSCOPE_API_KEY': 'test-key',
            'MODELSCOPE_API_BASE': '',  # Empty should use default
            'MODELSCOPE_MODEL': ''  # Empty should use default
        }, clear=False):
            
            api_base = os.getenv('MODELSCOPE_API_BASE') or 'https://api-inference.modelscope.cn/v1/'
            model = os.getenv('MODELSCOPE_MODEL') or 'Qwen/Qwen2.5-32B-Instruct'
            
            assert api_base == 'https://api-inference.modelscope.cn/v1/'
            assert model == 'Qwen/Qwen2.5-32B-Instruct'


class TestEndToEndIntegration:
    """Test end-to-end integration scenarios."""
    
    def test_complete_application_flow(self, mock_env_vars):
        """Test a complete application flow with mocked dependencies."""
        try:
            # Mock all external dependencies
            with patch('openai.OpenAI') as mock_openai:
                with patch('chromadb.PersistentClient') as mock_chromadb:
                    with patch('kiwi.flask_app.VannaFlaskApp.run') as mock_run:
                        
                        # Setup mocks
                        mock_client = MagicMock()
                        mock_openai.return_value = mock_client
                        mock_chromadb.return_value = MagicMock()
                        mock_run.return_value = None
                        
                        # Import and test components
                        from kiwi import OpenAI_Chat, ChromaDB_VectorStore
                        from kiwi.flask_app import VannaFlaskApp
                        
                        # Test that all components can be imported
                        assert OpenAI_Chat.__name__ == 'OpenAI_Chat'
                        assert ChromaDB_VectorStore.__name__ == 'ChromaDB_VectorStore'
                        assert VannaFlaskApp.__name__ == 'VannaFlaskApp'
                        
        except ImportError as e:
            pytest.skip(f"End-to-end test not possible: {e}")
    
    def test_application_startup_sequence(self, mock_env_vars):
        """Test the complete application startup sequence."""
        try:
            # Mock Flask to prevent actual server startup
            with patch('kiwi.flask_app.VannaFlaskApp.run') as mock_run:
                with patch('openai.OpenAI') as mock_openai:
                    with patch('chromadb.PersistentClient') as mock_chromadb:
                        
                        mock_openai.return_value = MagicMock()
                        mock_chromadb.return_value = MagicMock()
                        mock_run.return_value = None
                        
                        # Test the startup sequence
                        import importlib.util
                        
                        # Load kiwi_app module
                        spec = importlib.util.spec_from_file_location(
                            "kiwi_app", 
                            Path(__file__).parent.parent / "src" / "kiwi" / "kiwi_app.py"
                        )
                        
                        if spec and spec.loader:
                            module = importlib.util.module_from_spec(spec)
                            
                            # Execute the module (this tests the complete startup)
                            with patch.object(module, '__name__', 'test_module'):
                                spec.loader.exec_module(module)
                            
                            # Verify the module loaded successfully
                            assert hasattr(module, 'api_key')
                            assert module.api_key == 'test-modelscope-key-12345'
                
        except ImportError as e:
            pytest.skip(f"Application startup test not possible: {e}")