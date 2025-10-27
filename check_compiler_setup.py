# check_compiler_setup.py
import os

def check_compiler_setup():
    compiler_file = "src/core/compiler.py"
    
    if os.path.exists(compiler_file):
        print("📄 Checking compiler.py language registrations:")
        with open(compiler_file, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'self.languages' in line and '=' in line:
                    print(f"   Line {i+1}: {line.strip()}")
    
    print("\n🔍 Checking which language files exist:")
    languages_dir = "src/languages"
    if os.path.exists(languages_dir):
        for file in os.listdir(languages_dir):
            if file.endswith('.py') and not file.startswith('__'):
                print(f"   📄 {file}")

if __name__ == "__main__":
    check_compiler_setup()