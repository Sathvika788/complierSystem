# fix_method_signatures.py
import os

def fix_method_signatures():
    languages_dir = "src/languages"
    
    for file_name in ['python.py', 'javascript.py', 'java.py', 'go.py']:
        file_path = os.path.join(languages_dir, file_name)
        if os.path.exists(file_path):
            print(f"🔧 Fixing {file_name}...")
            
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Replace the execute method to handle both parameter names
            new_execute_method = '''
    def execute(self, code: str, input_data: str, timeout: int, memory_limit: int, **kwargs) -> Dict[str, Any]:
        """Handle both 'code' and 'source_code' parameters"""
        # If source_code is provided in kwargs, use it instead of code
        source_code = kwargs.get('source_code', code)
        return self.compile_code(source_code, input_data, timeout, memory_limit)
'''
            
            # Find and replace the execute method
            if 'def execute(self, code: str, input_data: str, timeout: int, memory_limit: int) -> Dict[str, Any]:' in content:
                content = content.replace(
                    'def execute(self, code: str, input_data: str, timeout: int, memory_limit: int) -> Dict[str, Any]:',
                    'def execute(self, code: str, input_data: str, timeout: int, memory_limit: int, **kwargs) -> Dict[str, Any]:'
                )
                # Replace the return line
                content = content.replace(
                    'return self.compile_code(code, input_data, timeout, memory_limit)',
                    'source_code = kwargs.get(\'source_code\', code)\n        return self.compile_code(source_code, input_data, timeout, memory_limit)'
                )
            
            with open(file_path, 'w') as f:
                f.write(content)
            
            print(f"✅ Fixed {file_name}")

if __name__ == "__main__":
    fix_method_signatures()