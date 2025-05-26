# Kiwi SQL Generation Project - Installation Guide

## Quick Start

### Basic Installation
Install the core dependencies for the Kiwi SQL generation project:

```bash
pip install -e .
```

### Full Installation
Install all optional dependencies for complete functionality:

```bash
pip install -e ".[all]"
```

## Installation Options

### Core Features Only
```bash
pip install -e .
```
Includes: Flask web app, LangChain/LangGraph, basic SQL generation

### Development Setup
```bash
pip install -e ".[dev,test]"
```
Includes: Core features + development tools (mypy, ruff, pytest, langgraph-cli)

### Database-Specific Installations

#### DuckDB (Recommended)
```bash
pip install -e ".[duckdb,chromadb,openai]"
```

#### PostgreSQL
```bash
pip install -e ".[postgres,chromadb,openai]"
```

#### MySQL
```bash
pip install -e ".[mysql,chromadb,openai]"
```

### FastAPI Alternative
If you prefer FastAPI over Flask:
```bash
pip install -e ".[fastapi,chromadb,openai]"
```

## System Requirements

- **Python**: 3.11 or higher (< 4.0)
- **Operating System**: Linux, macOS, or Windows
- **Memory**: Minimum 4GB RAM (8GB recommended for ChromaDB)
- **Storage**: At least 2GB free space for dependencies and data

## Environment Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Upgrade pip
```bash
pip install --upgrade pip
```

### 3. Install Kiwi
Choose one of the installation options above.

### 4. Environment Variables
Create a `.env` file in the project root:

```bash
# OpenAI API (if using OpenAI models)
OPENAI_API_KEY=your_openai_api_key_here

# ModelScope API (for Qwen models)
MODELSCOPE_API_KEY=your_modelscope_api_key_here

# Tavily Search (for web search capabilities)
TAVILY_API_KEY=your_tavily_api_key_here

# Database paths
DUCKDB_PATH=/path/to/your/database.db
CHROMADB_PATH=/path/to/chromadb/storage
```

## Running the Application

### Flask Web Application
```bash
cd /workspace/kiwi
python src/kiwi/kiwi_app.py
```

The application will be available at `http://localhost:12000`

### FastAPI Application (Alternative)
```bash
cd /workspace/kiwi
python -m uvicorn src.kiwi.fastapi.agent_app:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## Verification

### Test Installation
```bash
python -c "import kiwi; print('Kiwi installed successfully!')"
```

### Check Dependencies
```bash
pip check
```

### Test Web Interface
Navigate to `http://localhost:12000` and verify the interface loads.

### Test API Endpoints
```bash
curl http://localhost:12000/api/v0/get_config
```

## Troubleshooting

### Common Issues

#### 1. Protobuf Version Conflict
If you see protobuf-related errors:
```bash
pip install --upgrade protobuf>=5.29.0
```

#### 2. ChromaDB Installation Issues
On some systems, you may need to install additional dependencies:
```bash
# Ubuntu/Debian
sudo apt-get install build-essential

# macOS
xcode-select --install
```

#### 3. DuckDB Permission Issues
Ensure the DuckDB file path is writable:
```bash
chmod 755 /path/to/duckdb/directory
```

#### 4. Port Already in Use
If port 12000 is busy:
```bash
# Find and kill the process
lsof -ti:12000 | xargs kill -9

# Or use a different port
export FLASK_PORT=12001
```

### Getting Help

1. Check the [DEPENDENCY_ANALYSIS.md](./DEPENDENCY_ANALYSIS.md) for detailed dependency information
2. Review the application logs in `flask_app.log`
3. Ensure all environment variables are properly set
4. Verify database files exist and are accessible

## Development Setup

For contributors and developers:

```bash
# Clone the repository
git clone <repository-url>
cd kiwi

# Install in development mode with all dependencies
pip install -e ".[dev,test,all]"

# Run tests
pytest

# Run linting
ruff check src/

# Run type checking
mypy src/
```

## Production Deployment

For production environments:

1. Use a proper WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:12000 "src.kiwi.kiwi_app:app"
```

2. Set up proper environment variables
3. Configure database connections
4. Set up monitoring and logging
5. Use a reverse proxy (nginx) for SSL termination