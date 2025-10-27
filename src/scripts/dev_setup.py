#!/usr/bin/env python3
"""
Development setup script for VS Code
"""
import os
import subprocess
import sys
import venv
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running '{cmd}': {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running '{cmd}': {e}")
        return False

def setup_development_environment():
    """Setup complete development environment"""
    print("🚀 Setting up development environment...")
    
    # Create virtual environment
    if not Path("venv").exists():
        print("📦 Creating virtual environment...")
        venv.create("venv", with_pip=True)
    
    # Determine Python executable
    python_exe = "venv/Scripts/python.exe" if os.name == "nt" else "venv/bin/python"
    pip_exe = "venv/Scripts/pip.exe" if os.name == "nt" else "venv/bin/pip"
    
    # Install dependencies
    print("📚 Installing dependencies...")
    if not run_command(f"{pip_exe} install -r requirements-dev.txt"):
        print("❌ Failed to install dependencies")
        return False
    
    # Create .env file if it doesn't exist
    if not Path(".env").exists():
        print("🔧 Creating .env file...")
        with open(".env.example", "r") as f:
            env_content = f.read()
        with open(".env", "w") as f:
            f.write(env_content)
    
    # Run tests
    print("🧪 Running tests...")
    if run_command(f"{python_exe} -m pytest tests/ -v"):
        print("✅ Tests passed!")
    else:
        print("⚠️  Some tests failed, but continuing setup...")
    
    print("🎉 Development environment setup complete!")
    print("\nNext steps:")
    print("1. Start Redis: redis-server")
    print("2. Start API: Press F5 and select 'FastAPI Development Server'")
    print("3. Start Worker: Open new terminal and run 'python -m src.workers.queue_manager'")
    print("4. Open browser: http://localhost:8000/docs")

if __name__ == "__main__":
    setup_development_environment()