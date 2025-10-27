# quick_fix_compiler.py
import os

def quick_fix_compiler():
    compiler_file = "src/core/compiler.py"
    
    with open(compiler_file, 'r') as f:
        content = f.read()
    
    # Create backup
    with open(compiler_file + '.backup', 'w') as f:
        f.write(content)
    
    # Comment out problematic language registrations
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if any(x in line for x in ['CLanguage()', 'CppLanguage()', 'RustLanguage()', 'CSharpLanguage()', 'RubyLanguage()']):
            new_lines.append('# ' + line + '  # TEMPORARILY DISABLED')
        else:
            new_lines.append(line)
    
    new_content = '\n'.join(new_lines)
    
    with open(compiler_file, 'w') as f:
        f.write(new_content)
    
    print("✅ Temporarily disabled problematic languages")
    print("🔄 Only Python, JavaScript, Java, and Go will be available")

if __name__ == "__main__":
    quick_fix_compiler()