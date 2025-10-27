# check_language_registration.py
import os

def check_language_registration():
    compiler_file = "src/core/compiler.py"
    
    with open(compiler_file, 'r') as f:
        content = f.read()
        lines = content.split('\n')
        
        print("🔍 Language Registrations in compiler.py:")
        for i, line in enumerate(lines):
            if 'self.languages' in line and '=' in line:
                print(f"   Line {i+1}: {line.strip()}")

if __name__ == "__main__":
    check_language_registration()