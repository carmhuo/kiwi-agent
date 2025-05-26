#!/usr/bin/env python3
"""
Script to verify that FastAPI is properly set as an optional dependency.
This script should demonstrate that:
1. Core Kiwi functionality works without FastAPI
2. FastAPI modules fail gracefully when FastAPI is not installed
3. FastAPI modules work when FastAPI dependencies are installed
"""

import sys
import importlib.util

def check_core_imports():
    """Test that core Kiwi functionality can be imported without FastAPI."""
    print("🔍 Testing core imports (should work without FastAPI)...")
    
    try:
        # Test core modules
        import kiwi.base
        print("✅ Core base module imported successfully")
        
        import kiwi.openai_chat
        print("✅ OpenAI chat module imported successfully")
        
        import kiwi.chromadb_vector
        print("✅ ChromaDB vector module imported successfully")
        
        # Test Flask app
        from kiwi.flask_app import VannaFlaskApp
        print("✅ Flask app imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Core import failed: {e}")
        return False

def check_fastapi_imports():
    """Test FastAPI module imports."""
    print("\n🔍 Testing FastAPI imports...")
    
    # Check if FastAPI is available
    fastapi_available = importlib.util.find_spec("fastapi") is not None
    pydantic_available = importlib.util.find_spec("pydantic") is not None
    uvicorn_available = importlib.util.find_spec("uvicorn") is not None
    
    print(f"FastAPI available: {fastapi_available}")
    print(f"Pydantic available: {pydantic_available}")
    print(f"Uvicorn available: {uvicorn_available}")
    
    if fastapi_available and pydantic_available:
        try:
            # Test FastAPI modules
            from kiwi.fastapi.models import ChatRequest, MessageItem
            from kiwi.fastapi.agent_app import app
            from kiwi.fastapi.routers import router
            print("✅ FastAPI modules imported successfully")
            return True
        except ImportError as e:
            print(f"❌ FastAPI import failed despite dependencies being available: {e}")
            return False
    else:
        print("ℹ️  FastAPI dependencies not installed - this is expected for core-only installation")
        try:
            from kiwi.fastapi.models import ChatRequest
            print("❌ FastAPI modules should not import without dependencies")
            return False
        except ImportError:
            print("✅ FastAPI modules correctly fail to import without dependencies")
            return True

def main():
    """Main test function."""
    print("🧪 Testing Kiwi FastAPI Optional Dependency Configuration\n")
    
    # Test core functionality
    core_success = check_core_imports()
    
    # Test FastAPI functionality
    fastapi_success = check_fastapi_imports()
    
    print(f"\n📊 Results:")
    print(f"Core functionality: {'✅ PASS' if core_success else '❌ FAIL'}")
    print(f"FastAPI handling: {'✅ PASS' if fastapi_success else '❌ FAIL'}")
    
    if core_success and fastapi_success:
        print("\n🎉 All tests passed! FastAPI is properly configured as optional dependency.")
        return 0
    else:
        print("\n💥 Some tests failed. Check the configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())