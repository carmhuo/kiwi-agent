# Kiwi Project Testing Guide

## Overview

This guide describes the comprehensive testing structure for the Kiwi project, which has been optimized and moved to a dedicated `tests/` directory.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Shared pytest fixtures and configuration
├── test_environment_config.py  # Environment variable and configuration tests
├── test_integration.py         # Integration tests for component interaction
└── test_security.py           # Security compliance and vulnerability tests
```

## Test Categories

### 1. Environment Configuration Tests (`test_environment_config.py`)
- **Environment Variables**: Tests for required API keys and configuration
- **Dotenv Loading**: Tests for .env file loading and environment isolation
- **API Key Validation**: Tests for proper API key validation and error handling
- **Module Imports**: Tests for successful import of core components
- **Client Creation**: Tests for OpenAI and ModelScope client initialization

**Coverage**: 20 tests covering all environment setup scenarios

### 2. Integration Tests (`test_integration.py`)
- **Application Integration**: Tests for app initialization and startup
- **Vanna Integration**: Tests for Vanna AI component integration
- **Environment Integration**: Tests for dotenv and environment variable precedence
- **Error Handling Integration**: Tests for proper error propagation
- **Configuration Integration**: Tests for configuration consistency
- **End-to-End Integration**: Tests for complete application flow

**Coverage**: 12 tests (9 passed, 3 skipped) covering component interactions

### 3. Security Tests (`test_security.py`)
- **API Key Security**: Scans for hardcoded API keys in source code
- **Configuration Security**: Validates .env file exclusion and security
- **Error Handling Security**: Ensures error messages don't leak secrets
- **Dependency Security**: Checks for dangerous imports and configurations
- **Documentation Security**: Validates security mentions in documentation

**Coverage**: 12 tests ensuring security compliance

## Running Tests

### Quick Test Runner
```bash
# Run all tests with environment setup
python run_tests.py --all

# Run specific test categories
python run_tests.py --environment
python run_tests.py --security
python run_tests.py --integration
```

### Direct pytest Usage
```bash
# Run all tests
pytest tests/ -v

# Run specific test files
pytest tests/test_environment_config.py -v
pytest tests/test_security.py -v
pytest tests/test_integration.py -v

# Run with environment variables
MODELSCOPE_API_KEY=test-key pytest tests/ -v
```

## Test Configuration

### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### Environment Variables for Testing
- `MODELSCOPE_API_KEY`: Required for most tests (use test value)
- `OPENAI_API_KEY`: Optional for testing (can be unset)
- `FLASK_ENV`: Set to 'testing' for test runs

## Test Fixtures

### Shared Fixtures (`conftest.py`)
- `mock_env_vars`: Provides isolated environment variables for testing
- `temp_env_file`: Creates temporary .env files for dotenv testing
- `clean_environment`: Ensures clean environment state between tests

## Test Best Practices

### 1. Environment Isolation
- Tests use proper environment variable isolation
- Temporary files are cleaned up automatically
- Original environment state is restored after tests

### 2. Mocking External Dependencies
- OpenAI API calls are mocked to avoid real API usage
- ChromaDB connections are mocked for testing
- Flask app startup is mocked to prevent server conflicts

### 3. Error Handling
- Tests verify proper exception types and messages
- Error scenarios are thoroughly tested
- Security-sensitive error handling is validated

### 4. Security Compliance
- No hardcoded secrets in test files
- Pattern matching excludes known safe patterns (UUIDs, HTML attributes)
- Regular security scans for new vulnerabilities

## Test Results Summary

- **Total Tests**: 44 tests
- **Passed**: 41 tests
- **Skipped**: 3 tests (application startup tests that require special handling)
- **Failed**: 0 tests
- **Coverage**: Comprehensive coverage of all major components

## Continuous Integration

The test suite is designed to run in CI/CD environments:
- No external dependencies required for core tests
- Environment variables can be set in CI configuration
- Tests complete quickly (< 2 seconds total runtime)
- Clear pass/fail indicators for automated systems

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure PYTHONPATH includes the src directory
2. **Environment Variables**: Set MODELSCOPE_API_KEY for testing
3. **Module Not Found**: Install pytest with `pip install pytest`
4. **Permission Errors**: Ensure write access to test directories

### Debug Mode
```bash
# Run tests with detailed output
pytest tests/ -v -s --tb=long

# Run specific failing test
pytest tests/test_environment_config.py::TestEnvironmentVariables::test_modelscope_api_key_required -v
```

## Future Enhancements

1. **Performance Tests**: Add tests for response time and resource usage
2. **Load Tests**: Test application behavior under load
3. **Database Tests**: Add tests for data persistence and retrieval
4. **API Tests**: Add tests for REST API endpoints
5. **UI Tests**: Add tests for web interface functionality

## Contributing

When adding new tests:
1. Follow the existing naming conventions
2. Use appropriate test categories
3. Include proper documentation
4. Ensure environment isolation
5. Add security considerations
6. Update this guide as needed

---

For more information, see:
- [Environment Setup Guide](ENVIRONMENT_SETUP.md)
- [Security Audit Report](SECURITY_AUDIT_REPORT.md)
- [Project README](README.md)