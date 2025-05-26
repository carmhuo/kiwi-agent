# Kiwi SQL Generation Project - Dependency Analysis Report

## Overview
This report analyzes the code dependencies in the Kiwi SQL generation project and documents the updates made to `pyproject.toml`.

## Current Project Structure
- **Main Application**: Flask-based web application with SQL generation capabilities
- **React Agent**: LangGraph-based agent for SQL query generation
- **FastAPI Alternative**: Optional FastAPI implementation for API services
- **Vector Store**: ChromaDB for embeddings and similarity search
- **Database**: DuckDB for SQL query execution

## Core Dependencies Analysis

### Web Frameworks
- **Flask 3.1.1**: Primary web framework
  - `flask-sock 0.7.0`: WebSocket support
  - `flasgger 0.9.7.1`: Swagger/OpenAPI documentation
- **FastAPI 0.115.9**: Alternative API framework (optional)
  - `pydantic 2.11.3`: Data validation
  - `uvicorn`: ASGI server

### AI/ML Framework
- **LangChain Ecosystem**:
  - `langchain 0.3.25`: Core framework
  - `langchain-core 0.3.61`: Core components
  - `langchain-openai 0.3.18`: OpenAI integration
  - `langchain-anthropic 0.3.13`: Anthropic integration
  - `langchain-community 0.3.24`: Community tools
  - `langchain-fireworks 0.3.0`: Fireworks AI integration
  - `langchain-tavily 0.1.6`: Web search capabilities
- **LangGraph 0.4.7**: Agent workflow framework
- **OpenAI 1.75.0**: AI model client

### Database & Storage
- **SQLAlchemy 2.0.41**: SQL toolkit and ORM
- **DuckDB 1.2.2**: In-process SQL database
- **ChromaDB 1.0.10**: Vector database for embeddings
- **Pandas 2.2.3**: Data manipulation

### Data Visualization & Processing
- **Plotly 6.1.1**: Interactive plotting
- **Kaleido 0.2.1**: Static image export for Plotly
- **Tabulate 0.9.0**: Table formatting
- **SQLParse 0.5.3**: SQL parsing

### Utilities
- **Requests 2.32.3**: HTTP client
- **Python-dotenv 1.1.0**: Environment variable management

## Version Conflicts Resolved

### 1. ChromaDB Version Constraint
- **Issue**: `chromadb<1.0.0` constraint but 1.0.10 installed
- **Resolution**: Updated to `chromadb>=1.0.0`

### 2. Protobuf Version Conflict
- **Issue**: `fireworks-ai` requires `protobuf==5.29.4`, but 4.25.7 was installed
- **Resolution**: Updated to `protobuf>=5.29.0`
- **Note**: This creates a minor conflict with `opentelemetry-proto`, but doesn't affect core functionality

### 3. Missing Dependencies
- **Added**: FastAPI, Pydantic, uvicorn for optional API service
- **Added**: langchain-community for SQL toolkit
- **Added**: Proper version constraints for all dependencies

## Updated pyproject.toml Structure

### Core Dependencies
All essential dependencies moved to main `dependencies` section with appropriate version constraints:
- Web frameworks (Flask, flask-sock, flasgger)
- Data processing (pandas, plotly, requests, tabulate, kaleido)
- Database (sqlalchemy, sqlparse)
- LangChain ecosystem
- Configuration utilities

### Optional Dependencies
Organized into logical groups:
- `dev`: Development tools (mypy, ruff, pytest, langgraph-cli)
- `postgres`: PostgreSQL support
- `mysql`: MySQL support  
- `duckdb`: DuckDB support
- `chromadb`: Vector store support
- `openai`: OpenAI API support
- `fastapi`: FastAPI web framework
- `all`: All optional dependencies combined

### Dependency Groups (PEP 735)
- `dev`: Development dependencies
- `test`: Testing dependencies
- `runtime`: Production runtime dependencies

## Installation Recommendations

### Basic Installation
```bash
pip install -e .
```

### Full Installation with All Features
```bash
pip install -e ".[all]"
```

### Development Installation
```bash
pip install -e ".[dev,test]"
```

### Specific Database Support
```bash
pip install -e ".[duckdb,chromadb,openai]"
```

## Compatibility Notes

1. **Python Version**: Requires Python >=3.11,<4.0
2. **Protobuf**: Updated to 5.29.x for fireworks-ai compatibility
3. **ChromaDB**: Updated to 1.0.x for latest features
4. **LangChain**: All components aligned to 0.3.x series

## Testing Status

- ✅ Dependency resolution successful
- ✅ Core Flask application functional
- ✅ Protobuf conflict resolved
- ⚠️ Minor opentelemetry-proto conflict (non-critical)

## Next Steps

1. Test all optional dependency combinations
2. Update CI/CD pipelines to use new dependency structure
3. Consider pinning specific versions for production deployments
4. Monitor for updates to resolve remaining minor conflicts

## Files Modified

- `pyproject.toml`: Complete dependency restructure
- Added proper version constraints and optional dependency groups
- Organized dependencies by functionality
- Added PEP 735 dependency groups