#!/usr/bin/env python3
"""
Simple test script to verify the frontend structure and integration
"""

import os
import sys
from pathlib import Path

def test_frontend_structure():
    """Test that all frontend files are in place"""
    print("🧪 Testing Frontend Structure...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    required_files = [
        "package.json",
        "vite.config.js",
        "build.py",
        "README.md",
        "src/templates/base/index.html",
        "src/templates/chat/chat.html",
        "src/templates/dashboard/dashboard.html",
        "src/assets/css/base.css",
        "src/assets/css/chat.css",
        "src/assets/css/dashboard.css",
        "src/assets/js/main.js",
        "src/assets/js/modules/api.js",
        "src/assets/js/modules/chat.js",
        "src/assets/js/modules/utils.js",
        "src/components/Button.js",
        "src/components/Modal.js",
        "src/components/index.js"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = frontend_dir / file_path
        if not full_path.exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All frontend files are present!")
    return True

def test_imports():
    """Test that all Python imports work"""
    print("\n🧪 Testing Python Imports...")
    
    try:
        from src.kiwi.base import VannaBase
        print("✅ VannaBase import successful")
    except ImportError as e:
        print(f"❌ VannaBase import failed: {e}")
        return False
    
    try:
        from src.kiwi.frontend_integration import FrontendIntegration
        print("✅ FrontendIntegration import successful")
    except ImportError as e:
        print(f"❌ FrontendIntegration import failed: {e}")
        return False
    
    try:
        from src.kiwi.flask_app.frontend_app import create_app
        print("✅ create_app import successful")
    except ImportError as e:
        print(f"❌ create_app import failed: {e}")
        return False
    
    print("✅ All imports successful!")
    return True

def test_build_system():
    """Test the build system"""
    print("\n🧪 Testing Build System...")
    
    build_script = Path("frontend/build.py")
    if not build_script.exists():
        print("❌ Build script not found")
        return False
    
    # Test if build script is executable
    if not os.access(build_script, os.X_OK):
        print("⚠️  Build script is not executable, making it executable...")
        os.chmod(build_script, 0o755)
    
    print("✅ Build system ready!")
    return True

def main():
    """Run all tests"""
    print("🥝 Kiwi Frontend Structure Test\n")
    
    tests = [
        test_frontend_structure,
        test_imports,
        test_build_system
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All tests passed! Frontend structure is ready.")
        return 0
    else:
        print("❌ Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())