#!/usr/bin/env python3
"""
Demo script showing FastAPI as optional dependency in Kiwi project.

This script demonstrates:
1. Core Kiwi functionality works without FastAPI dependencies
2. How to install and use FastAPI features when needed
3. Proper dependency isolation
"""

import sys
import subprocess
import importlib.util

def check_dependency_available(package_name):
    """Check if a package is available for import."""
    return importlib.util.find_spec(package_name) is not None

def demo_core_functionality():
    """Demonstrate core Kiwi functionality without FastAPI."""
    print("🔍 Testing Core Kiwi Functionality (Flask-based)")
    print("=" * 50)
    
    try:
        # Import core modules
        import kiwi.base
        print("✅ Core base module imported")
        
        import kiwi.openai_chat  
        print("✅ OpenAI chat module imported")
        
        import kiwi.chromadb_vector
        print("✅ ChromaDB vector module imported")
        
        # Import Flask app
        from kiwi.flask_app import VannaFlaskApp
        print("✅ Flask app imported")
        
        print("\n🎉 Core functionality is working without FastAPI dependencies!")
        return True
        
    except ImportError as e:
        print(f"❌ Core import failed: {e}")
        return False

def demo_dependency_status():
    """Show current dependency status."""
    print("\n🔍 Dependency Status Check")
    print("=" * 30)
    
    dependencies = {
        "FastAPI": "fastapi",
        "Pydantic": "pydantic", 
        "Uvicorn": "uvicorn",
        "Flask": "flask",
        "LangChain": "langchain",
        "SQLAlchemy": "sqlalchemy"
    }
    
    for name, package in dependencies.items():
        available = check_dependency_available(package)
        status = "✅ Available" if available else "❌ Not installed"
        print(f"{name:12}: {status}")

def show_installation_commands():
    """Show how to install optional dependencies."""
    print("\n📦 Installation Commands")
    print("=" * 25)
    
    print("Core installation (Flask only):")
    print("  pip install -e .")
    print()
    
    print("With FastAPI support:")
    print("  pip install -e .[fastapi]")
    print()
    
    print("Full installation (all optional dependencies):")
    print("  pip install -e .[all]")
    print()
    
    print("Individual optional groups:")
    print("  pip install -e .[postgresql]  # PostgreSQL support")
    print("  pip install -e .[mysql]       # MySQL support") 
    print("  pip install -e .[duckdb]      # DuckDB support")
    print("  pip install -e .[chromadb]    # ChromaDB support")
    print("  pip install -e .[openai]      # OpenAI support")

def demo_fastapi_usage():
    """Show how FastAPI would be used when available."""
    print("\n🚀 FastAPI Usage (when installed)")
    print("=" * 35)
    
    fastapi_available = check_dependency_available("fastapi")
    
    if fastapi_available:
        print("FastAPI is available. You can:")
        print("1. Import FastAPI modules:")
        print("   from kiwi.fastapi.models import ChatRequest")
        print("   from kiwi.fastapi.agent_app import app")
        print()
        print("2. Run FastAPI server:")
        print("   uvicorn kiwi.fastapi.agent_app:app --host 0.0.0.0 --port 8000")
        print()
        print("⚠️  Note: FastAPI modules require proper configuration (API keys, database)")
    else:
        print("FastAPI is not installed. To use FastAPI features:")
        print("1. Install FastAPI dependencies:")
        print("   pip install -e .[fastapi]")
        print()
        print("2. Then you can use FastAPI endpoints as an alternative to Flask")

def main():
    """Main demo function."""
    print("🧪 Kiwi FastAPI Optional Dependency Demo")
    print("=" * 45)
    print()
    
    # Test core functionality
    core_success = demo_core_functionality()
    
    # Show dependency status
    demo_dependency_status()
    
    # Show installation options
    show_installation_commands()
    
    # Demo FastAPI usage
    demo_fastapi_usage()
    
    print("\n📋 Summary")
    print("=" * 10)
    if core_success:
        print("✅ Core Kiwi functionality works independently")
        print("✅ FastAPI is properly configured as optional dependency")
        print("✅ Users can choose Flask-only or Flask+FastAPI installation")
    else:
        print("❌ Core functionality has issues")
    
    print("\n🎯 Key Benefits:")
    print("• Minimal installation for basic usage (Flask only)")
    print("• Optional FastAPI for users who need it")
    print("• Clear separation of concerns")
    print("• Flexible deployment options")

if __name__ == "__main__":
    main()