# check_base_signature.py
import os

def check_base_signature():
    base_file = "src/languages/base.py"
    if os.path.exists(base_file):
        print("📄 BaseLanguage method signatures:")
        with open(base_file, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'def ' in line and ('execute' in line or 'compile_code' in line):
                    print(f"   Line {i+1}: {line.strip()}")

if __name__ == "__main__":
    check_base_signature()