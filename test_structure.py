#!/usr/bin/env python3
"""
Test script to verify project structure and imports
"""

import sys
import os
from pathlib import Path

def test_structure():
    """Test if all required directories and files exist"""
    print("[*] Testing project structure...")
    
    required_dirs = [
        "src",
        "src/config",
        "src/services",
        "src/utils",
        "k8s",
        ".github/workflows",
        "public/static",
    ]
    
    required_files = [
        "src/main.py",
        "src/process_docs.py",
        "src/config/settings.py",
        "src/services/rag_service.py",
        "src/utils/helpers.py",
        "requirements.txt",
        ".env.example",
        "Dockerfile",
        "docker-compose.yml",
        ".gitignore",
        ".dockerignore",
        "README.md",
        "DEPLOYMENT.md",
        "k8s/deployment.yaml",
        "k8s/service.yaml",
    ]
    
    errors = []
    
    # Check directories
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            errors.append(f"[X] Missing directory: {dir_path}")
        else:
            print(f"[OK] Directory exists: {dir_path}")
    
    # Check files
    for file_path in required_files:
        if not Path(file_path).exists():
            errors.append(f"[X] Missing file: {file_path}")
        else:
            print(f"[OK] File exists: {file_path}")
    
    return errors

def test_imports():
    """Test if Python imports work"""
    print("\n[*] Testing Python imports...")
    
    errors = []
    
    try:
        from src.config import settings
        print("[OK] Import src.config.settings")
    except Exception as e:
        errors.append(f"[X] Failed to import src.config.settings: {e}")
    
    try:
        from src.utils.helpers import normalize_query, get_base64_image
        print("[OK] Import src.utils.helpers")
    except Exception as e:
        errors.append(f"[X] Failed to import src.utils.helpers: {e}")
    
    try:
        from src.services.rag_service import setup_rag_chain
        print("[OK] Import src.services.rag_service")
    except Exception as e:
        errors.append(f"[X] Failed to import src.services.rag_service: {e}")
    
    return errors

def test_env():
    """Test environment configuration"""
    print("\n[*] Testing environment configuration...")
    
    errors = []
    
    if not Path(".env.example").exists():
        errors.append("[X] .env.example not found")
    else:
        print("[OK] .env.example exists")
    
    if Path(".env").exists():
        print("[OK] .env file exists")
    else:
        print("[!] .env file not found (create from .env.example)")
    
    return errors

def main():
    print("=" * 60)
    print("FCAJ Chatbot - Project Structure Test")
    print("=" * 60)
    
    all_errors = []
    
    # Run tests
    all_errors.extend(test_structure())
    all_errors.extend(test_imports())
    all_errors.extend(test_env())
    
    # Summary
    print("\n" + "=" * 60)
    if all_errors:
        print("[FAILED] TESTS FAILED")
        print("\nErrors found:")
        for error in all_errors:
            print(f"  {error}")
        sys.exit(1)
    else:
        print("[SUCCESS] ALL TESTS PASSED!")
        print("\nProject structure is correct!")
        print("\nNext steps:")
        print("  1. Copy .env.example to .env and add your API key")
        print("  2. Run: python src/process_docs.py")
        print("  3. Run: streamlit run src/main.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
