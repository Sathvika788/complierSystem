# find_compilers.py
import subprocess
import os

def find_compilers():
    print("🔍 Finding Installed Compilers...")
    
    # Common installation paths on Windows
    common_paths = [
        r"C:\Program Files\mingw-w64\*\mingw64\bin",
        r"C:\mingw\bin", 
        r"C:\Program Files\Java\*\bin",
        r"C:\Program Files\OpenJDK\*\bin",
        r"C:\Program Files\Go\bin",
        r"C:\Users\{}\.cargo\bin".format(os.getenv('USERNAME')),
        r"C:\Program Files\dotnet",
        r"C:\Program Files\Ruby*\bin",
        r"C:\tools\ruby*\bin"
    ]
    
    found_compilers = {}
    
    for path_pattern in common_paths:
        # Expand wildcards and user directory
        expanded_path = os.path.expandvars(path_pattern)
        if "*" in expanded_path:
            import glob
            matches = glob.glob(expanded_path)
            for match in matches:
                if os.path.exists(match):
                    compiler = check_path_for_compilers(match)
                    if compiler:
                        found_compilers.update(compiler)
        else:
            if os.path.exists(expanded_path):
                compiler = check_path_for_compilers(expanded_path)
                if compiler:
                    found_compilers.update(compiler)
    
    print("\n📋 Found Compilers:")
    for name, path in found_compilers.items():
        print(f"✅ {name}: {path}")
    
    return found_compilers

def check_path_for_compilers(path):
    compilers = {
        "gcc.exe": "C Compiler",
        "g++.exe": "C++ Compiler", 
        "javac.exe": "Java Compiler",
        "go.exe": "Go Compiler",
        "rustc.exe": "Rust Compiler",
        "dotnet.exe": ".NET SDK",
        "ruby.exe": "Ruby"
    }
    
    found = {}
    for exe, name in compilers.items():
        exe_path = os.path.join(path, exe)
        if os.path.exists(exe_path):
            found[name] = exe_path
    
    return found

if __name__ == "__main__":
    find_compilers()