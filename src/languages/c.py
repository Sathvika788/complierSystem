# src/languages/c.py
import os
import tempfile
import subprocess
from typing import Dict, Any
from .base import BaseLanguage

class CLanguage(BaseLanguage):
    def compile_code(self, code: str, input_data: str, timeout: int, memory_limit: int) -> Dict[str, Any]:
        try:
            # Create temporary C file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False, encoding='utf-8') as src_file:
                src_file.write(code)
                src_path = src_file.name
            
            # Compile C code
            compile_process = subprocess.run(
                ['gcc', src_path, '-o', src_path + '.exe'],
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
            
            # Execute compiled program
            exec_process = subprocess.run(
                [src_path + '.exe'],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            # Cleanup
            try:
                os.unlink(src_path)
                os.unlink(src_path + '.exe')
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