# src/languages/csharp.py
import os
import tempfile
import subprocess
from typing import Dict, Any
from src.languages.base import BaseLanguage

class CSharpLanguage(BaseLanguage):
    @property
    def name(self) -> str:
        return "C#"
    
    @property
    def extension(self) -> str:
        return ".cs"
    
    def compile_code(self, code: str, input_data: str, timeout: int, memory_limit: int) -> Dict[str, Any]:
        return {
            'success': False,
            'output': '',
            'error': 'C# compiler coming soon!',
            'exit_code': -1
        }
    
    def execute(self, code: str, input_data: str, timeout: int, memory_limit: int) -> Dict[str, Any]:
        return self.compile_code(code, input_data, timeout, memory_limit)