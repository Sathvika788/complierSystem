# src/languages/rust.py
import os
import tempfile
import subprocess
from typing import Dict, Any
from src.languages.base import BaseLanguage

class RustLanguage(BaseLanguage):
    @property
    def name(self) -> str:
        return "Rust"
    
    @property
    def extension(self) -> str:
        return ".rs"
    
    def compile_code(self, code: str, input_data: str, timeout: int, memory_limit: int) -> Dict[str, Any]:
        return {
            'success': False,
            'output': '',
            'error': 'Rust compiler coming soon!',
            'exit_code': -1
        }
    
    def execute(self, code: str, input_data: str, timeout: int, memory_limit: int) -> Dict[str, Any]:
        return self.compile_code(code, input_data, timeout, memory_limit)