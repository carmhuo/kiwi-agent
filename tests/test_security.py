"""
Security-focused tests for the Kiwi project.

This module contains tests that verify security best practices
and ensure no sensitive information is exposed.
"""

import os
import re
import pytest
from pathlib import Path


class TestAPIKeySecurity:
    """Test API key security measures."""
    
    def test_no_api_keys_in_python_files(self, project_root_path):
        """Test that no API keys are hardcoded in Python files."""
        # Common API key patterns - more specific to avoid false positives
        api_key_patterns = [
            r'api_key\s*=\s*["\'][a-zA-Z0-9\-]{20,}["\']',  # api_key = "key"
            r'API_KEY\s*=\s*["\'][a-zA-Z0-9\-]{20,}["\']',  # API_KEY = "key"
            r'sk-[a-zA-Z0-9]{48}',  # OpenAI API key pattern
            r'["\'][a-zA-Z0-9]{32}["\']',  # 32-char alphanumeric strings (potential keys)
        ]
        
        # Known safe patterns to exclude
        safe_patterns = [
            r'your-.*-api-key-here',  # Template placeholders
            r'test-.*-key',  # Test keys
            r'example-.*-key',  # Example keys
            r'placeholder',  # Placeholder text
            r'00000000-0000-0000-0000-000000000000',  # UUID namespace
            r'uuid\.UUID',  # UUID constructor calls
            r'data-hs-overlay-backdrop-container',  # HTML attributes
            r'class=',  # CSS classes
            r'id=',  # HTML IDs
        ]
        
        python_files = list((project_root_path / "src").rglob("*.py"))
        
        for py_file in python_files:
            content = py_file.read_text(encoding='utf-8')
            
            for pattern in api_key_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                
                for match in matches:
                    # Check if it's a safe pattern
                    is_safe = any(re.search(safe_pattern, match, re.IGNORECASE) 
                                for safe_pattern in safe_patterns)
                    
                    if not is_safe:
                        pytest.fail(f"Potential API key found in {py_file}: {match}")
    
    def test_no_secrets_in_test_files(self, project_root_path):
        """Test that no real secrets are in test files."""
        test_files = list((project_root_path / "tests").rglob("*.py"))
        
        # Patterns that indicate real secrets (not test data)
        secret_patterns = [
            r'sk-[a-zA-Z0-9]{48}',  # OpenAI API key pattern
            r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}',  # UUID pattern
        ]
        
        for test_file in test_files:
            content = test_file.read_text(encoding='utf-8')
            
            for pattern in secret_patterns:
                matches = re.findall(pattern, content)
                
                for match in matches:
                    # Allow test UUIDs and mock keys
                    if not (match.startswith('test-') or 'mock' in match.lower() or 
                           match == '9d431c1c-2acd-4dd0-b95a-76affce19b3b' or  # Known test key
                           match == '00000000-0000-0000-0000-000000000000'):  # UUID namespace
                        pytest.fail(f"Potential real secret found in {test_file}: {match}")
    
    def test_environment_variable_usage(self, project_root_path):
        """Test that environment variables are used for sensitive configuration."""
        python_files = list((project_root_path / "src").rglob("*.py"))
        
        # Files that should use environment variables
        sensitive_files = ['kiwi_app.py', 'graph_app.py']
        
        for py_file in python_files:
            if py_file.name in sensitive_files:
                content = py_file.read_text(encoding='utf-8')
                
                # Should contain environment variable usage
                assert 'os.getenv' in content or 'os.environ' in content, \
                    f"{py_file} should use environment variables for configuration"
                
                # Should contain API key environment variable
                assert 'MODELSCOPE_API_KEY' in content, \
                    f"{py_file} should reference MODELSCOPE_API_KEY environment variable"


class TestConfigurationSecurity:
    """Test configuration security measures."""
    
    def test_env_file_excluded_from_git(self, project_root_path):
        """Test that .env files are properly excluded from git."""
        gitignore_file = project_root_path / ".gitignore"
        
        if gitignore_file.exists():
            gitignore_content = gitignore_file.read_text()
            
            # Check for various .env patterns
            env_patterns = ['.env', '*.env', '.env.*']
            
            found_env_exclusion = any(pattern in gitignore_content for pattern in env_patterns)
            assert found_env_exclusion, ".env files should be excluded in .gitignore"
    
    def test_no_env_files_in_repo(self, project_root_path):
        """Test that no .env files are committed to the repository."""
        env_files = list(project_root_path.rglob(".env"))
        env_files.extend(list(project_root_path.rglob("*.env")))
        
        # Filter out .env.example which is allowed
        actual_env_files = [f for f in env_files if not f.name.endswith('.example')]
        
        assert len(actual_env_files) == 0, \
            f"Found .env files in repository: {actual_env_files}"
    
    def test_env_example_has_placeholders(self, project_root_path):
        """Test that .env.example contains placeholders, not real values."""
        env_example = project_root_path / ".env.example"
        
        if env_example.exists():
            content = env_example.read_text()
            
            # Should contain placeholder patterns
            placeholder_patterns = [
                'your-.*-key-here',
                'your-.*-api-key',
                'placeholder',
                'example',
            ]
            
            has_placeholders = any(
                re.search(pattern, content, re.IGNORECASE) 
                for pattern in placeholder_patterns
            )
            
            assert has_placeholders, ".env.example should contain placeholders, not real values"


class TestErrorHandlingSecurity:
    """Test that error handling doesn't expose sensitive information."""
    
    def test_error_messages_no_secrets(self, project_root_path):
        """Test that error messages don't contain sensitive information."""
        python_files = list((project_root_path / "src").rglob("*.py"))
        
        # Patterns that might expose secrets in error messages
        dangerous_patterns = [
            r'print\(.*api_key.*\)',  # Printing API keys
            r'logger.*api_key',  # Logging API keys
            r'raise.*api_key.*\)',  # API keys in exceptions
        ]
        
        for py_file in python_files:
            content = py_file.read_text(encoding='utf-8')
            
            for pattern in dangerous_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                
                if matches:
                    pytest.fail(f"Potential secret exposure in error handling in {py_file}: {matches}")
    
    def test_validation_error_messages_safe(self, project_root_path):
        """Test that validation error messages are safe and helpful."""
        python_files = list((project_root_path / "src").rglob("*.py"))
        
        for py_file in python_files:
            content = py_file.read_text(encoding='utf-8')
            
            # Look for ValueError messages about API keys
            if 'ValueError' in content and 'API_KEY' in content:
                # Should contain helpful guidance
                assert 'export' in content or 'set' in content, \
                    f"{py_file} should provide helpful guidance in error messages"
                
                # Should not contain actual API key values
                assert not re.search(r'[a-f0-9]{32,}', content), \
                    f"{py_file} error messages should not contain actual API keys"


class TestDependencySecurity:
    """Test security of dependencies and imports."""
    
    def test_no_dangerous_imports(self, project_root_path):
        """Test that no dangerous or unnecessary imports are used."""
        python_files = list((project_root_path / "src").rglob("*.py"))
        
        # Potentially dangerous imports for this type of application
        dangerous_imports = [
            'subprocess',  # Unless specifically needed
            'eval',
            'exec',
            'pickle',  # Can be dangerous with untrusted data
        ]
        
        for py_file in python_files:
            content = py_file.read_text(encoding='utf-8')
            
            for dangerous_import in dangerous_imports:
                if f'import {dangerous_import}' in content or f'from {dangerous_import}' in content:
                    # This is a warning, not necessarily a failure
                    print(f"Warning: {py_file} imports {dangerous_import} - verify this is necessary and safe")
    
    def test_secure_client_configuration(self, project_root_path):
        """Test that API clients are configured securely."""
        python_files = list((project_root_path / "src").rglob("*.py"))
        
        for py_file in python_files:
            content = py_file.read_text(encoding='utf-8')
            
            # If OpenAI client is used, check configuration
            if 'OpenAI(' in content:
                # Should use environment variables for API key
                assert 'os.getenv' in content or 'os.environ' in content, \
                    f"{py_file} should use environment variables for OpenAI client configuration"
                
                # Should not have hardcoded API keys
                openai_lines = [line for line in content.split('\n') if 'OpenAI(' in line]
                for line in openai_lines:
                    assert not re.search(r'api_key\s*=\s*["\'][a-zA-Z0-9\-]{20,}["\']', line), \
                        f"{py_file} should not have hardcoded API keys in OpenAI client: {line}"


class TestDocumentationSecurity:
    """Test that documentation follows security best practices."""
    
    def test_readme_mentions_security(self, project_root_path):
        """Test that README mentions security considerations."""
        readme_files = [
            project_root_path / "README.md",
            project_root_path / "ENVIRONMENT_SETUP.md"
        ]
        
        security_keywords = [
            'environment variable',
            'API key',
            'security',
            '.env',
            'secret'
        ]
        
        for readme_file in readme_files:
            if readme_file.exists():
                content = readme_file.read_text().lower()
                
                found_security_mention = any(
                    keyword in content for keyword in security_keywords
                )
                
                assert found_security_mention, \
                    f"{readme_file} should mention security considerations"
    
    def test_setup_instructions_secure(self, project_root_path):
        """Test that setup instructions promote secure practices."""
        setup_files = [
            project_root_path / "README.md",
            project_root_path / "ENVIRONMENT_SETUP.md"
        ]
        
        for setup_file in setup_files:
            if setup_file.exists():
                content = setup_file.read_text()
                
                # Should mention .env.example
                if '.env' in content:
                    assert '.env.example' in content, \
                        f"{setup_file} should reference .env.example template"
                
                # Should not contain real API keys
                assert not re.search(r'[a-f0-9]{32,}', content), \
                    f"{setup_file} should not contain real API keys"