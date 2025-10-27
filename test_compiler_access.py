# test_compiler_access_fixed.py
import os
import subprocess
import tempfile

def test_compiler_access_fixed():
    print("🔧 Testing Compiler Access - FIXED")
    
    # Test multiple possible locations
    compiler_locations = [
        # Chocolatey locations
        r"C:\ProgramData\mingw64\mingw64\bin",
        r"C:\tools\mingw64\bin",
        # MSYS2 locations
        r"C:\msys64\mingw64\bin",
        # Manual locations
        r"C:\mingw64\bin",
        r"C:\MinGW\bin"
    ]
    
    found_compilers = []
    
    for base_path in compiler_locations:
        print(f"\n🔍 Checking: {base_path}")
        if os.path.exists(base_path):
            print(f"✅ Path exists")
            
            gcc_path = os.path.join(base_path, "gcc.exe")
            gpp_path = os.path.join(base_path, "g++.exe")
            
            if os.path.exists(gcc_path):
                print(f"🎯 GCC found: {gcc_path}")
                found_compilers.append(("GCC", gcc_path))
                
                # Test version
                try:
                    result = subprocess.run([gcc_path, "--version"], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        version = result.stdout.split('\n')[0]
                        print(f"✅ GCC working: {version}")
                    else:
                        print(f"❌ GCC test failed")
                except Exception as e:
                    print(f"❌ GCC error: {e}")
            
            if os.path.exists(gpp_path):
                print(f"🎯 G++ found: {gpp_path}")
                found_compilers.append(("G++", gpp_path))
                
                # Test version
                try:
                    result = subprocess.run([gpp_path, "--version"], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        version = result.stdout.split('\n')[0]
                        print(f"✅ G++ working: {version}")
                    else:
                        print(f"❌ G++ test failed")
                except Exception as e:
                    print(f"❌ G++ error: {e}")
        else:
            print(f"❌ Path not found")
    
    # Test PATH
    print(f"\n🔍 Checking PATH...")
    try:
        result = subprocess.run(['gcc', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ GCC found in PATH")
            found_compilers.append(("GCC", "PATH"))
    except:
        print("❌ GCC not in PATH")
    
    try:
        result = subprocess.run(['g++', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ G++ found in PATH")
            found_compilers.append(("G++", "PATH"))
    except:
        print("❌ G++ not in PATH")
    
    return found_compilers

def test_simple_compilation():
    print(f"\n🧪 Testing Simple Compilation...")
    
    test_c_code = '''#include <stdio.h>
int main() {
    printf("Hello from C!\\\\n");
    return 0;
}
'''
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False, encoding='utf-8') as f:
            f.write(test_c_code)
            c_file = f.name
        
        # Try different compiler paths
        compiler_paths = [
            r"C:\ProgramData\mingw64\mingw64\bin\gcc.exe",
            r"C:\tools\mingw64\bin\gcc.exe", 
            r"C:\msys64\mingw64\bin\gcc.exe",
            r"C:\mingw64\bin\gcc.exe",
            "gcc"  # Try PATH
        ]
        
        for compiler in compiler_paths:
            if compiler == "gcc" or os.path.exists(compiler):
                print(f"🔧 Trying compiler: {compiler}")
                try:
                    result = subprocess.run([compiler, c_file, '-o', c_file + '.exe'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        print("✅ Compilation successful!")
                        # Execute
                        exec_result = subprocess.run([c_file + '.exe'], capture_output=True, text=True, timeout=5)
                        print(f"✅ Execution output: {exec_result.stdout.strip()}")
                        break
                    else:
                        print(f"❌ Compilation failed: {result.stderr[:100]}...")
                except Exception as e:
                    print(f"❌ Compiler error: {e}")
        
        # Cleanup
        try:
            os.unlink(c_file)
            if os.path.exists(c_file + '.exe'):
                os.unlink(c_file + '.exe')
        except:
            pass
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    found = test_compiler_access_fixed()
    if found:
        print(f"\n🎯 Found {len(found)} compilers:")
        for name, path in found:
            print(f"   {name}: {path}")
    else:
        print(f"\n❌ No compilers found")
    
    test_simple_compilation()