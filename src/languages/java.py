# src/languages/java.py
import os
import tempfile
import subprocess
from typing import Dict, Any
from src.languages.base import BaseLanguage

class JavaLanguage(BaseLanguage):
    @property
    def name(self) -> str:
        return "Java"
    
    @property
    def extension(self) -> str:
        return ".java"
    
    def compile_code(self, code: str, input_data: str, timeout: int, memory_limit: int) -> Dict[str, Any]:
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False, encoding='utf-8') as src_file:
                src_file.write(code)
                src_path = src_file.name
            
            class_name = "Main"
            for line in code.split('\n'):
                if 'class' in line and '{' in line:
                    parts = line.split()
                    if 'class' in parts:
                        class_idx = parts.index('class')
                        if class_idx + 1 < len(parts):
                            class_name = parts[class_idx + 1]
                            if '{' in class_name:
                                class_name = class_name.split('{')[0]
                            break
            
            compile_process = subprocess.run(
                ['javac', src_path],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if compile_process.returncode != 0:
                return {
                    'success': False,
                    'output': '',
                    'error': compile_process.stderr,
                    'exit_code': compile_process.returncode
                }
            
            class_dir = os.path.dirname(src_path)
            exec_process = subprocess.run(
                ['java', '-cp', class_dir, class_name],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            try:
                os.unlink(src_path)
                class_file = os.path.join(class_dir, f"{class_name}.class")
                if os.path.exists(class_file):
                    os.unlink(class_file)
            except:
                pass
            
            return {
                'success': True,
                'output': exec_process.stdout,
                'error': exec_process.stderr,
                'exit_code': exec_process.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'output': '',
                'error': 'Execution timeout',
                'exit_code': -1
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'exit_code': -1
            }
    
    def execute(self, code: str, input_data: str, timeout: int, memory_limit: int) -> Dict[str, Any]:
        return self.compile_code(code, input_data, timeout, memory_limit)