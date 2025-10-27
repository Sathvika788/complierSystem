# fix_go_registration.py
import os

def fix_go_registration():
    compiler_file = "src/core/compiler.py"
    
    with open(compiler_file, 'r') as f:
        content = f.read()
    
    # Check if Go is registered
    if 'self.languages[1]' not in content or '# self.languages[1]' in content:
        print("🔧 Fixing Go language registration...")
        
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            if '# self.languages[1]' in line and 'GoLanguage' in line:
                # Uncomment the Go registration
                new_lines.append(line.replace('# ', ''))
            else:
                new_lines.append(line)
        
        new_content = '\n'.join(new_lines)
        
        with open(compiler_file, 'w') as f:
            f.write(new_content)
        
        print("✅ Go language registration fixed")
    else:
        print("✅ Go language is already registered")

if __name__ == "__main__":
    fix_go_registration()