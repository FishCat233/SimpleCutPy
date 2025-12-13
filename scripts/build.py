#!/usr/bin/env python
import os
import subprocess
import sys

def main():
    """Simple build script for SimpleCutPy"""
    print("SimpleCutPy Build Script")
    print("========================================")
    
    # Change to project root directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    os.chdir(project_root)
    
    # Clean build directories
    print("Cleaning build directories...")
    for dir_name in ["build", "dist"]:
        dir_path = os.path.join(project_root, dir_name)
        if os.path.exists(dir_path):
            import shutil
            shutil.rmtree(dir_path)
            print(f"  ✅ Cleaned {dir_name} directory")
    
    # Install dependencies
    print("Installing dependencies...")
    result = subprocess.run(["uv", "sync"], check=True)
    if result.returncode != 0:
        print("❌ Dependency installation failed")
        sys.exit(1)
    
    # Build application
    print("Building application...")
    result = subprocess.run(["pyinstaller", "SimpleCutPy.spec"], check=True)
    if result.returncode != 0:
        print("❌ Application build failed")
        sys.exit(1)
    
    # Check build result
    print("Checking build result...")
    exe_path = os.path.join(project_root, "dist", "SimpleCutPy.exe")
    if os.path.exists(exe_path):
        print(f"✅ Build successful: {exe_path}")
    else:
        print("❌ Build failed: Executable not found")
        sys.exit(1)
    
    print("Build completed!")

if __name__ == "__main__":
    main()
