# GitHub Workflows Documentation

This directory contains optimized GitHub Actions workflows for the Kiwi SQL Generation Project. These workflows provide comprehensive CI/CD, security scanning, and code quality checks.

## 🔄 Workflows Overview

### 1. CI (unit-tests.yml)
**Triggers:** Push to main, Pull requests, Manual dispatch

**Jobs:**
- **Lint and Type Check**: Runs ruff linting, formatting checks, and mypy type checking
- **Spell Check**: Checks spelling in README and source code using codespell
- **Unit Tests**: Runs pytest across multiple OS (Ubuntu, Windows, macOS) and Python versions (3.11, 3.12)
- **Frontend Tests**: Lints, formats, and builds the frontend code

**Key Features:**
- ✅ Multi-platform testing (Linux, Windows, macOS)
- ✅ Code coverage reporting with Codecov integration
- ✅ Parallel job execution for faster feedback
- ✅ Proper dependency caching for faster builds
- ✅ GitHub-formatted output for better PR integration

### 2. Integration Tests (integration-tests.yml)
**Triggers:** Daily schedule, Push/PR on relevant paths, Manual dispatch

**Jobs:**
- **Integration Tests**: Runs integration tests with external services

**Key Features:**
- ✅ Scheduled daily runs to catch external service issues
- ✅ Path-based triggering to avoid unnecessary runs
- ✅ Automatic issue creation on scheduled test failures
- ✅ Test artifact upload for debugging
- ✅ Timeout protection (30 minutes)
- ✅ Environment variable management for API keys

### 3. Security (security.yml)
**Triggers:** Push to main, Pull requests, Weekly schedule, Manual dispatch

**Jobs:**
- **Dependency Check**: Runs safety and bandit security scans
- **Semgrep**: Advanced static analysis security scanning
- **CodeQL**: GitHub's semantic code analysis

**Key Features:**
- ✅ Multiple security scanning tools
- ✅ Weekly scheduled scans
- ✅ Security report artifacts
- ✅ SARIF upload for GitHub Security tab integration

### 4. Code Quality (code-quality.yml)
**Triggers:** Push to main, Pull requests, Weekly schedule, Manual dispatch

**Jobs:**
- **Code Quality Analysis**: Comprehensive code quality metrics
- **Performance Testing**: Benchmark and performance tests

**Key Features:**
- ✅ Code coverage analysis with branch coverage
- ✅ Cyclomatic complexity analysis
- ✅ Documentation coverage checking
- ✅ Dead code detection
- ✅ Import sorting validation
- ✅ PR comments with quality metrics
- ✅ Coverage badges generation

### 5. Dependency Update (dependency-update.yml)
**Triggers:** Weekly schedule (Mondays), Manual dispatch

**Jobs:**
- **Update Python Dependencies**: Updates Python packages
- **Update Frontend Dependencies**: Updates npm packages

**Key Features:**
- ✅ Automated dependency updates
- ✅ Separate PRs for Python and frontend dependencies
- ✅ Draft PRs for manual review
- ✅ Before/after comparison reports
- ✅ Security fix application

### 6. Release (release.yml)
**Triggers:** Version tags (v*.*.*), Manual dispatch with version input

**Jobs:**
- **Validate Release**: Version format validation
- **Test Before Release**: Full test suite before release
- **Build Package**: Python package building and validation
- **Build Frontend**: Frontend build for distribution
- **Create Release**: GitHub release creation with changelog
- **Publish PyPI**: Automated PyPI publishing

**Key Features:**
- ✅ Automated release process
- ✅ Version validation
- ✅ Pre-release testing
- ✅ Automatic changelog generation
- ✅ PyPI publishing with trusted publishing
- ✅ Frontend build artifacts

## 🔧 Configuration Requirements

### Repository Secrets
The following secrets should be configured in your repository:

#### Required for Integration Tests:
- `ANTHROPIC_API_KEY`: Anthropic API key for AI services
- `OPENAI_API_KEY`: OpenAI API key for AI services
- `TAVILY_API_KEY`: Tavily API key for search services
- `LANGSMITH_API_KEY`: LangSmith API key for tracing

#### Required for Release:
- `PYPI_API_TOKEN`: PyPI API token for package publishing

### Repository Settings
1. **Branch Protection**: Enable branch protection for `main` branch
2. **Required Status Checks**: Configure required checks for PRs
3. **Trusted Publishing**: Set up PyPI trusted publishing for releases

## 📊 Key Improvements Made

### 1. **Dependency Management**
- ✅ Fixed incorrect `uv pip install -r pyproject.toml` usage
- ✅ Proper installation with `uv pip install -e ".[dev,test]"`
- ✅ Consistent dependency group usage

### 2. **Test Path Corrections**
- ✅ Fixed test paths to match actual directory structure
- ✅ Updated from `tests/unit_tests` to `tests/`
- ✅ Corrected integration test path

### 3. **Action Updates**
- ✅ Updated to latest action versions (checkout@v5, setup-python@v5)
- ✅ Added proper caching for faster builds
- ✅ Implemented astral-sh/setup-uv@v4 for better uv management

### 4. **Security Enhancements**
- ✅ Added explicit permissions for each workflow
- ✅ Implemented security scanning workflows
- ✅ Added dependency vulnerability checking

### 5. **Code Quality**
- ✅ Comprehensive code quality metrics
- ✅ Coverage reporting with badges
- ✅ Complexity analysis
- ✅ Documentation coverage tracking

### 6. **Frontend Integration**
- ✅ Added frontend testing and building
- ✅ Proper Node.js setup and caching
- ✅ Frontend dependency management

### 7. **Release Automation**
- ✅ Complete release pipeline
- ✅ Automated changelog generation
- ✅ PyPI publishing with trusted publishing
- ✅ Version validation

## 🚀 Usage Examples

### Running Tests Locally
```bash
# Install dependencies
uv venv
uv pip install -e ".[dev,test]"

# Run unit tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src --cov-report=html

# Run linting
uv run ruff check .
uv run ruff format --check .
uv run mypy src/
```

### Creating a Release
1. Create and push a version tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
2. The release workflow will automatically:
   - Validate the version
   - Run full test suite
   - Build packages
   - Create GitHub release
   - Publish to PyPI

### Manual Workflow Triggers
All workflows support manual triggering via GitHub UI:
1. Go to Actions tab
2. Select the workflow
3. Click "Run workflow"
4. Fill in any required inputs

## 📈 Monitoring and Maintenance

### Regular Tasks
- **Weekly**: Review dependency update PRs
- **Monthly**: Review security scan results
- **Quarterly**: Update workflow action versions

### Troubleshooting
- Check workflow logs in GitHub Actions tab
- Review artifact uploads for detailed reports
- Monitor security alerts in GitHub Security tab
- Check code coverage trends over time

## 🔗 Related Documentation
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [uv Documentation](https://docs.astral.sh/uv/)
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [CodeQL Documentation](https://codeql.github.com/docs/)