# src/languages/go.py
import os
import tempfile
import subprocess
from typing import Dict, Any
from src.languages.base import BaseLanguage

class GoLanguage(BaseLanguage):
    @property
    def name(self) -> str:
        return "Go"
    
    @property
    def extension(self) -> str:
        return ".go"
    
    def compile_code(self, code: str, input_data: str, timeout: int, memory_limit: int) -> Dict[str, Any]:
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False, encoding='utf-8') as src_file:
                src_file.write(code)
                src_path = src_file.name
            
            exec_process = subprocess.run(
                ['go', 'run', src_path],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            try:
                os.unlink(src_path)
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