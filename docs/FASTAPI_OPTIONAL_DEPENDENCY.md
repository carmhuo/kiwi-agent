# FastAPI Optional Dependency Configuration

## Overview

The Kiwi SQL generation project has been configured to make FastAPI an optional dependency, allowing users to choose between a minimal Flask-only installation or a full installation with both Flask and FastAPI support.

## Architecture

### Core Dependencies (Always Installed)
- **Flask**: Primary web framework for the main application
- **LangChain ecosystem**: Core AI/ML functionality
- **SQLAlchemy**: Database abstraction layer
- **Data processing**: pandas, plotly, requests, etc.

### Optional Dependencies
- **FastAPI group**: FastAPI, Pydantic, uvicorn (for alternative API endpoints)
- **Database groups**: PostgreSQL, MySQL, DuckDB, ChromaDB drivers
- **AI services**: OpenAI API client

## Installation Options

### 1. Minimal Installation (Flask only)
```bash
pip install -e .
```
This installs only the core dependencies needed for the Flask application.

### 2. With FastAPI Support
```bash
pip install -e .[fastapi]
```
This adds FastAPI, Pydantic, and uvicorn to the core installation.

### 3. Full Installation
```bash
pip install -e .[all]
```
This installs all optional dependencies for complete functionality.

### 4. Custom Combinations
```bash
# Flask + PostgreSQL + OpenAI
pip install -e .[postgresql,openai]

# Flask + FastAPI + DuckDB + ChromaDB
pip install -e .[fastapi,duckdb,chromadb]
```

## Usage Patterns

### Flask-Only Usage (Default)
```python
# Core functionality always available
from kiwi.flask_app import VannaFlaskApp
from kiwi.base import VannaBase
from kiwi.openai_chat import OpenAI_Chat

# Run Flask app
app = VannaFlaskApp()
app.run(host='0.0.0.0', port=5000)
```

### FastAPI Usage (When Installed)
```python
# Only available when fastapi group is installed
from kiwi.fastapi.agent_app import app
from kiwi.fastapi.models import ChatRequest

# Run with uvicorn
# uvicorn kiwi.fastapi.agent_app:app --host 0.0.0.0 --port 8000
```

## Benefits

### For End Users
1. **Smaller installation**: Core functionality without unnecessary dependencies
2. **Faster setup**: Reduced download and installation time
3. **Fewer conflicts**: Less chance of dependency version conflicts
4. **Choice**: Pick the web framework that suits your needs

### For Developers
1. **Modular architecture**: Clear separation between core and optional features
2. **Easier testing**: Can test core functionality independently
3. **Flexible deployment**: Different deployment scenarios supported
4. **Maintainability**: Easier to manage dependencies

## Technical Implementation

### pyproject.toml Structure
```toml
[project]
dependencies = [
    # Core web framework (Flask only)
    "flask>=3.0.0",
    "flask-sock>=0.7.0",
    "flasgger>=0.9.7",
    
    # Core LangChain and data processing
    "langgraph>=0.3.0",
    "langchain>=0.3.0",
    # ... other core dependencies
]

[project.optional-dependencies]
# FastAPI web framework (optional alternative to Flask)
fastapi = [
    "fastapi>=0.115.0",
    "pydantic>=2.11.0",
    "uvicorn[standard]>=0.30.0",
]

# Other optional groups...
all = [
    # Includes all optional dependencies
]
```

### Dependency Isolation
- Core modules (`kiwi.base`, `kiwi.openai_chat`, etc.) have no FastAPI dependencies
- FastAPI modules (`kiwi.fastapi.*`) are isolated in their own package
- Flask app works independently of FastAPI installation status

## Migration Guide

### From Previous Versions
If you were using a version where FastAPI was a core dependency:

1. **No changes needed** if you only use Flask features
2. **Add `[fastapi]` to installation** if you use FastAPI endpoints:
   ```bash
   pip install -e .[fastapi]
   ```

### For New Projects
1. Start with minimal installation: `pip install -e .`
2. Add optional dependencies as needed
3. Use Flask for web UI, FastAPI for API endpoints (optional)

## Troubleshooting

### ImportError for FastAPI modules
```python
# Error: ModuleNotFoundError: No module named 'fastapi'
from kiwi.fastapi.agent_app import app
```

**Solution**: Install FastAPI dependencies
```bash
pip install -e .[fastapi]
```

### Checking Installation Status
```python
import importlib.util

def check_fastapi_available():
    return importlib.util.find_spec("fastapi") is not None

if check_fastapi_available():
    from kiwi.fastapi.agent_app import app
    print("FastAPI is available")
else:
    print("FastAPI not installed - using Flask only")
```

## Testing

Run the demo script to verify the configuration:
```bash
python demo_optional_fastapi.py
```

This will show:
- Core functionality status
- Available dependencies
- Installation options
- Usage examples

## Future Considerations

1. **Lazy imports**: Consider lazy importing in FastAPI modules to avoid initialization issues
2. **Configuration**: Add runtime checks for required environment variables
3. **Documentation**: Keep installation instructions updated
4. **CI/CD**: Test both minimal and full installations in CI pipeline

## Conclusion

The FastAPI optional dependency configuration provides flexibility while maintaining backward compatibility. Users can choose the installation that best fits their needs, from minimal Flask-only setups to full-featured installations with both web frameworks.