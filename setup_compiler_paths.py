# setup_compiler_paths.py
import os
import subprocess

def setup_compiler_paths():
    print("🛠️ Setting up Compiler Paths...")
    
    # Paths we found
    compiler_paths = [
        r"C:\Program Files\OpenJDK\jdk-25\bin",      # Java
        r"C:\Program Files\Go\bin",                  # Go
        r"C:\Program Files\dotnet",                  # .NET
        r"C:\tools\ruby34\bin",                      # Ruby
        # MinGW paths to try
        r"C:\Program Files\mingw-w64\*\mingw64\bin",
        r"C:\mingw\bin",
        r"C:\mingw64\bin"
    ]
    
    # Add to current PATH
    current_path = os.environ.get('PATH', '')
    added_paths = []
    
    for path in compiler_paths:
        if '*' in path:
            import glob
            matches = glob.glob(path)
            for match in matches:
                if os.path.exists(match) and match not in current_path:
                    os.environ['PATH'] = match + ';' + os.environ['PATH']
                    added_paths.append(match)
        else:
            if os.path.exists(path) and path not in current_path:
                os.environ['PATH'] = path + ';' + os.environ['PATH']
                added_paths.append(path)
    
    print("✅ Added to PATH:")
    for path in added_paths:
        print(f"   📁 {path}")
    
    return added_paths

def test_compilers():
    print("\n🧪 Testing Compilers...")
    
    compilers = {
        "Java": "javac -version",
        "Go": "go version", 
        ".NET": "dotnet --version",
        "Ruby": "ruby --version"
    }
    
    for name, cmd in compilers.items():
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ {name}: Working - {result.stdout.strip()}")
            else:
                print(f"❌ {name}: Failed - {result.stderr.strip()}")
        except Exception as e:
            print(f"❌ {name}: Error - {e}")

if __name__ == "__main__":
    added_paths = setup_compiler_paths()
    if added_paths:
        print("\n🔄 Please RESTART VS CODE to apply PATH changes!")
    test_compilers()