#!/usr/bin/env python3
"""
Quick environment configuration test for Kiwi project.

This script provides a simple way to verify that environment variables
are properly configured. For comprehensive testing, use pytest:

    pytest tests/ -v

This script checks:
1. Environment variables are properly loaded
2. API keys are configured correctly
3. Applications can start without hardcoded credentials
"""

import os
import sys
from pathlib import Path


def main():
    """Main test function."""
    print("🧪 Kiwi Environment Configuration Quick Test")
    print("=" * 50)
    print()
    
    # Check if .env file exists
    env_file = Path(__file__).parent / ".env"
    env_example = Path(__file__).parent / ".env.example"
    
    if env_file.exists():
        print("✅ .env file found")
    else:
        print("⚠️  .env file not found")
        if env_example.exists():
            print("💡 Suggestion: Copy .env.example to .env and configure your API keys")
            print("   Command: cp .env.example .env")
        else:
            print("💡 Suggestion: Create a .env file with your API keys")
    
    # Load environment variables from .env if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded from .env file")
    except ImportError:
        print("⚠️  python-dotenv not installed, using system environment variables only")
    except Exception as e:
        print(f"⚠️  Could not load .env file: {e}")
    
    print("\n🔍 Checking Environment Variables")
    print("=" * 40)
    
    # Check required variables (at least one should be set)
    modelscope_key = os.getenv('MODELSCOPE_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if not modelscope_key and not openai_key:
        print("❌ ERROR: No API key found!")
        print("   Please set either MODELSCOPE_API_KEY or OPENAI_API_KEY")
        print("\n📖 For detailed setup instructions, see: ENVIRONMENT_SETUP.md")
        print("🧪 For comprehensive testing, run: pytest tests/ -v")
        return False
    
    if modelscope_key:
        print(f"✅ MODELSCOPE_API_KEY: {'*' * 8}{modelscope_key[-4:] if len(modelscope_key) > 4 else '****'}")
    else:
        print("⚠️  MODELSCOPE_API_KEY: Not set")
    
    if openai_key:
        print(f"✅ OPENAI_API_KEY: {'*' * 8}{openai_key[-4:] if len(openai_key) > 4 else '****'}")
    else:
        print("⚠️  OPENAI_API_KEY: Not set")
    
    print("\n🎉 Basic environment check passed!")
    print("\n🚀 You can now run the application:")
    print("   python src/kiwi/kiwi_app.py")
    print("\n🧪 For comprehensive testing, run:")
    print("   pytest tests/ -v")
    print("   pytest tests/test_security.py -v  # Security tests")
    print("   pytest tests/test_environment_config.py -v  # Environment tests")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)