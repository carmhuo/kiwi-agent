#!/usr/bin/env python3
"""
Test runner script for Kiwi project.

This script provides different ways to run tests:
- Quick environment check
- Full test suite
- Security tests only
- Environment tests only
- Integration tests only
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_quick_test():
    """Run quick environment configuration test."""
    print("🚀 Running quick environment test...")
    try:
        # Get the script directory and project root
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        test_script = script_dir / "test_env_config.py"
        
        result = subprocess.run([sys.executable, str(test_script)], 
                              cwd=str(project_root),
                              capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False


def run_pytest(test_path=None, markers=None, verbose=True):
    """Run pytest with specified options."""
    # Get the project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    cmd = [sys.executable, "-m", "pytest"]
    
    if test_path:
        cmd.append(test_path)
    else:
        cmd.append(str(project_root / "tests"))
    
    if verbose:
        cmd.append("-v")
    
    if markers:
        cmd.extend(["-m", markers])
    
    print(f"🧪 Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, cwd=str(project_root), capture_output=False, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        print("❌ pytest not found. Install with: pip install pytest")
        return False
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False


def check_pytest_available():
    """Check if pytest is available."""
    try:
        subprocess.run([sys.executable, "-m", "pytest", "--version"], 
                      capture_output=True, text=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run tests for Kiwi project")
    parser.add_argument("--quick", action="store_true", 
                       help="Run quick environment test only")
    parser.add_argument("--security", action="store_true", 
                       help="Run security tests only")
    parser.add_argument("--environment", action="store_true", 
                       help="Run environment configuration tests only")
    parser.add_argument("--integration", action="store_true", 
                       help="Run integration tests only")
    parser.add_argument("--all", action="store_true", 
                       help="Run all tests (default)")
    parser.add_argument("--no-pytest", action="store_true", 
                       help="Skip pytest tests even if available")
    
    args = parser.parse_args()
    
    print("🧪 Kiwi Project Test Runner")
    print("=" * 30)
    print()
    
    # Check if we're in the right directory
    if not Path("src/kiwi").exists():
        print("❌ Error: Please run this script from the project root directory")
        return False
    
    success = True
    
    # Quick test
    if args.quick:
        return run_quick_test()
    
    # Always run quick test first
    print("1️⃣ Running quick environment check...")
    if not run_quick_test():
        print("❌ Quick test failed. Please fix environment configuration first.")
        return False
    
    print("\n" + "=" * 50)
    
    # Check if pytest is available
    if not args.no_pytest and check_pytest_available():
        print("2️⃣ Running comprehensive tests with pytest...")
        
        if args.security:
            success = run_pytest("tests/test_security.py")
        elif args.environment:
            success = run_pytest("tests/test_environment_config.py")
        elif args.integration:
            success = run_pytest("tests/test_integration.py")
        else:
            # Run all tests
            success = run_pytest()
    
    else:
        if not args.no_pytest:
            print("⚠️  pytest not available. Install with: pip install pytest")
        print("✅ Quick test passed. For comprehensive testing, install pytest.")
    
    print("\n" + "=" * 50)
    
    if success:
        print("🎉 All tests passed!")
        print("\n📋 Next steps:")
        print("   • Run the application: python src/kiwi/kiwi_app.py")
        print("   • Check documentation: ENVIRONMENT_SETUP.md")
        print("   • Review security: SECURITY_AUDIT_REPORT.md")
    else:
        print("❌ Some tests failed. Please check the output above.")
        print("\n📖 For help:")
        print("   • Environment setup: ENVIRONMENT_SETUP.md")
        print("   • Run specific tests: python run_tests.py --security")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)