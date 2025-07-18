#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test runner script for the entire project.
This script runs all implemented tests from one place.
"""

import sys
import subprocess
import os
from pathlib import Path


def main():
    """Run all tests in the project."""
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Change to project directory
    os.chdir(project_root)
    
    print("=" * 80)
    print("Running all tests for the project")
    print("=" * 80)
    
    # Run pytest with verbose output
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v",
            "--tb=short",
            "--color=yes"
        ], check=False, capture_output=False)
        
        print("\n" + "=" * 80)
        if result.returncode == 0:
            print("✅ All tests passed successfully!")
        else:
            print("❌ Some tests failed. Check the output above for details.")
        print("=" * 80)
        
        return result.returncode
        
    except FileNotFoundError:
        print("❌ Error: pytest not found. Please install pytest:")
        print("   pip install pytest")
        return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())