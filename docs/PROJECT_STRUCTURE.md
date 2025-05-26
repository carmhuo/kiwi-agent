# Kiwi Project Structure

This document describes the optimized project structure for the Kiwi application.

## Directory Structure

```
kiwi/
├── docs/                           # Documentation files
│   ├── DEPENDENCY_ANALYSIS.md      # Dependency analysis and management
│   ├── ENVIRONMENT_SETUP.md        # Environment setup guide
│   ├── FASTAPI_OPTIONAL_DEPENDENCY.md  # FastAPI optional dependency info
│   ├── FRONTEND_OPTIMIZATION.md    # Frontend optimization guide
│   ├── INSTALLATION.md             # Installation instructions
│   ├── PROJECT_STRUCTURE.md        # This file
│   └── TESTING_GUIDE.md           # Comprehensive testing guide
├── frontend/                       # Frontend application
│   ├── src/                       # Frontend source files
│   ├── dist/                      # Built frontend assets
│   ├── package.json               # Node.js dependencies
│   ├── vite.config.js            # Vite configuration
│   └── README.md                  # Frontend-specific documentation
├── logs/                          # Application log files
├── scripts/                       # Utility and test scripts
│   ├── check_optional_fastapi.py  # FastAPI dependency checker
│   ├── demo_optional_fastapi.py   # FastAPI demo script
│   ├── run_frontend_demo.py       # Frontend demo runner
│   ├── run_tests.py              # Test runner script
│   ├── test_env_config.py        # Quick environment test
│   └── test_frontend.py          # Frontend structure test
├── src/kiwi/                      # Main application source code
│   ├── exceptions/                # Custom exception classes
│   ├── fastapi/                   # FastAPI application components
│   │   ├── agent_app.py          # FastAPI agent application
│   │   ├── models.py             # Pydantic models
│   │   └── routers.py            # API route definitions
│   ├── flask_app/                 # Flask application components
│   │   ├── assets.py             # Static asset management
│   │   ├── auth.py               # Authentication logic
│   │   └── frontend_app.py       # Flask frontend application
│   ├── react_agent/               # LangGraph React agent
│   │   ├── configuration.py      # Agent configuration
│   │   ├── graph.py              # Agent graph definition
│   │   ├── prompts.py            # Agent prompts
│   │   ├── state.py              # Agent state management
│   │   ├── tools.py              # Agent tools
│   │   └── utils.py              # Agent utilities
│   ├── react_app/                 # Flask React application
│   │   ├── customer_graph.py     # Customer-specific graph
│   │   ├── graph.py              # Application graph
│   │   └── routes.py             # Flask routes
│   ├── types/                     # Type definitions
│   ├── base.py                    # Base classes and interfaces
│   ├── chromadb_vector.py         # ChromaDB vector store
│   ├── config.py                  # Configuration management
│   ├── frontend_integration.py    # Frontend integration utilities
│   ├── graph_app.py              # Graph application logic
│   ├── kiwi_app.py               # Main application entry point
│   ├── openai_chat.py            # OpenAI chat integration
│   ├── run_react_app.py          # React app runner
│   └── utils.py                  # General utilities
├── static/                        # Static assets
├── tests/                         # Test suite
│   ├── conftest.py               # Test configuration and fixtures
│   ├── test_environment_config.py # Environment configuration tests
│   ├── test_integration.py       # Integration tests
│   └── test_security.py          # Security compliance tests
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── LICENSE                        # Project license
├── Makefile                       # Build automation
├── README.md                      # Main project documentation
├── langgraph.json                 # LangGraph configuration
├── pyproject.toml                 # Python project configuration
└── pytest.ini                    # Pytest configuration
```

## Component Overview

### Core Application (`src/kiwi/`)
- **Main Entry Point**: `kiwi_app.py` - Primary application launcher
- **Configuration**: `config.py` - Centralized configuration management
- **Base Classes**: `base.py` - Abstract base classes and interfaces

### Web Applications
- **FastAPI App**: `fastapi/` - Modern async API with automatic documentation
- **Flask App**: `flask_app/` - Traditional web application with templates
- **React App**: `react_app/` - Flask-based React integration

### AI/ML Components
- **React Agent**: `react_agent/` - LangGraph-based reasoning agent
- **Vector Store**: `chromadb_vector.py` - ChromaDB integration
- **Chat Integration**: `openai_chat.py` - OpenAI API integration

### Frontend (`frontend/`)
- **Modern Frontend**: Vite-based build system with React components
- **Static Assets**: Built and optimized frontend resources
- **Development Tools**: Hot reload and development server

### Testing (`tests/`)
- **Environment Tests**: Configuration and environment variable validation
- **Security Tests**: Security compliance and vulnerability scanning
- **Integration Tests**: End-to-end component testing

### Documentation (`docs/`)
- **Setup Guides**: Installation and environment configuration
- **Architecture**: Project structure and component relationships
- **Testing**: Comprehensive testing documentation

### Utilities (`scripts/`)
- **Test Runners**: Automated testing and validation scripts
- **Demo Scripts**: Example usage and demonstration code
- **Development Tools**: Development and debugging utilities

## Key Features

### 1. **Modular Architecture**
- Clear separation of concerns between web frameworks
- Pluggable AI/ML components
- Independent frontend and backend development

### 2. **Multiple Web Framework Support**
- FastAPI for modern async APIs
- Flask for traditional web applications
- React integration for modern UIs

### 3. **Comprehensive Testing**
- Environment configuration validation
- Security compliance checking
- Integration testing across components

### 4. **Developer Experience**
- Hot reload for frontend development
- Automated testing and validation
- Clear documentation and examples

### 5. **Production Ready**
- Environment-based configuration
- Security best practices
- Logging and monitoring support

## Development Workflow

1. **Setup**: Follow `docs/INSTALLATION.md` for initial setup
2. **Configuration**: Use `docs/ENVIRONMENT_SETUP.md` for environment variables
3. **Testing**: Run `scripts/run_tests.py` for comprehensive testing
4. **Development**: Use appropriate app runner for your use case
5. **Frontend**: Use `frontend/` directory for UI development

## Entry Points

- **Main Application**: `python src/kiwi/kiwi_app.py`
- **FastAPI Server**: `python src/kiwi/fastapi/agent_app.py`
- **Flask Application**: `python src/kiwi/run_react_app.py`
- **Frontend Development**: `cd frontend && npm run dev`
- **Testing**: `python scripts/run_tests.py`

## Configuration

All configuration is managed through environment variables. See:
- `.env.example` for required variables
- `docs/ENVIRONMENT_SETUP.md` for detailed setup
- `src/kiwi/config.py` for configuration logic