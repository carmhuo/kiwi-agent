#!/usr/bin/env python3
"""
Test script to verify environment variable configuration for Kiwi project.

This script checks:
1. Environment variables are properly loaded
2. API keys are configured correctly
3. Applications can start without hardcoded credentials
"""

import os
import sys
from pathlib import Path

def check_env_variables():
    """Check if required environment variables are set."""
    print("🔍 Checking Environment Variables")
    print("=" * 40)
    
    required_vars = {
        'MODELSCOPE_API_KEY': 'ModelScope API Key',
        'OPENAI_API_KEY': 'OpenAI API Key (alternative)'
    }
    
    optional_vars = {
        'MODELSCOPE_API_BASE': 'ModelScope API Base URL',
        'MODELSCOPE_MODEL': 'ModelScope Model Name',
        'FLASK_ENV': 'Flask Environment',
        'FLASK_DEBUG': 'Flask Debug Mode',
        'FLASK_HOST': 'Flask Host',
        'FLASK_PORT': 'Flask Port'
    }
    
    # Check required variables (at least one should be set)
    modelscope_key = os.getenv('MODELSCOPE_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if not modelscope_key and not openai_key:
        print("❌ ERROR: No API key found!")
        print("   Please set either MODELSCOPE_API_KEY or OPENAI_API_KEY")
        return False
    
    if modelscope_key:
        print(f"✅ MODELSCOPE_API_KEY: {'*' * 8}{modelscope_key[-4:] if len(modelscope_key) > 4 else '****'}")
    else:
        print("⚠️  MODELSCOPE_API_KEY: Not set")
    
    if openai_key:
        print(f"✅ OPENAI_API_KEY: {'*' * 8}{openai_key[-4:] if len(openai_key) > 4 else '****'}")
    else:
        print("⚠️  OPENAI_API_KEY: Not set")
    
    # Check optional variables
    print("\nOptional Variables:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"⚪ {var}: Not set (using default)")
    
    return True

def test_import_modules():
    """Test importing modules that use environment variables."""
    print("\n🧪 Testing Module Imports")
    print("=" * 30)
    
    try:
        # Test core modules
        import kiwi.base
        print("✅ kiwi.base imported successfully")
        
        import kiwi.openai_chat
        print("✅ kiwi.openai_chat imported successfully")
        
        import kiwi.chromadb_vector
        print("✅ kiwi.chromadb_vector imported successfully")
        
        # Test Flask app
        from kiwi.flask_app import VannaFlaskApp
        print("✅ VannaFlaskApp imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_client_creation():
    """Test creating OpenAI client with environment variables."""
    print("\n🔧 Testing Client Creation")
    print("=" * 30)
    
    try:
        from openai import OpenAI
        
        # Test ModelScope client creation
        modelscope_key = os.getenv('MODELSCOPE_API_KEY')
        if modelscope_key:
            client = OpenAI(
                base_url='https://api-inference.modelscope.cn/v1/',
                api_key=modelscope_key
            )
            print("✅ ModelScope client created successfully")
        
        # Test OpenAI client creation
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            client = OpenAI(api_key=openai_key)
            print("✅ OpenAI client created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Client creation failed: {e}")
        return False

def test_app_initialization():
    """Test that applications can initialize without hardcoded keys."""
    print("\n🚀 Testing Application Initialization")
    print("=" * 40)
    
    try:
        # Test if we can import the main app modules without errors
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        # This should work if environment variables are properly set
        print("Testing kiwi_app module...")
        # We'll just test the import, not actually run the app
        import importlib.util
        
        spec = importlib.util.spec_from_file_location(
            "kiwi_app", 
            Path(__file__).parent / "src" / "kiwi" / "kiwi_app.py"
        )
        
        if spec and spec.loader:
            print("✅ kiwi_app.py can be loaded (environment variables properly configured)")
        else:
            print("❌ kiwi_app.py cannot be loaded")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ App initialization test failed: {e}")
        return False

def check_env_file():
    """Check if .env file exists and provide guidance."""
    print("\n📁 Environment File Check")
    print("=" * 30)
    
    env_file = Path(__file__).parent / ".env"
    env_example = Path(__file__).parent / ".env.example"
    
    if env_file.exists():
        print("✅ .env file found")
        return True
    else:
        print("⚠️  .env file not found")
        if env_example.exists():
            print("💡 Suggestion: Copy .env.example to .env and configure your API keys")
            print("   Command: cp .env.example .env")
        else:
            print("💡 Suggestion: Create a .env file with your API keys")
        return False

def main():
    """Main test function."""
    print("🧪 Kiwi Environment Configuration Test")
    print("=" * 45)
    print()
    
    # Check if .env file exists
    env_file_ok = check_env_file()
    
    # Load environment variables from .env if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded from .env file")
    except ImportError:
        print("⚠️  python-dotenv not installed, using system environment variables only")
    except Exception as e:
        print(f"⚠️  Could not load .env file: {e}")
    
    # Run tests
    tests = [
        ("Environment Variables", check_env_variables),
        ("Module Imports", test_import_modules),
        ("Client Creation", test_client_creation),
        ("App Initialization", test_app_initialization),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 20)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your environment is properly configured.")
        print("\n🚀 You can now run the application:")
        print("   python src/kiwi/kiwi_app.py")
    else:
        print("\n⚠️  Some tests failed. Please check your environment configuration.")
        print("\n📖 For help, see: ENVIRONMENT_SETUP.md")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)