# src/languages/c_cpp.py
import os
import tempfile
import subprocess
from typing import Dict, Any
from src.languages.base import BaseLanguage

class CLanguage(BaseLanguage):
    @property
    def name(self) -> str:
        return "C"
    
    @property
    def extension(self) -> str:
        return ".c"
    
    def _find_compiler(self):
        """Find GCC compiler using known Chocolatey location"""
        # Known Chocolatey MinGW location
        known_paths = [
            r"C:\ProgramData\mingw64\mingw64\bin\gcc.exe",
            r"C:\tools\mingw64\bin\gcc.exe"
        ]
        
        for compiler_path in known_paths:
            if os.path.exists(compiler_path):
                print(f"🎯 Found GCC at: {compiler_path}")
                return compiler_path
        
        # Also try PATH
        try:
            subprocess.run(['gcc', '--version'], capture_output=True, timeout=2)
            print("🎯 Found GCC in PATH")
            return 'gcc'
        except:
            pass
        
        print("❌ GCC compiler not found")
        return None
    
    def compile_code(self, code: str, input_data: str, timeout: int, memory_limit: int) -> Dict[str, Any]:
        compiler = self._find_compiler()
        
        if not compiler:
            return {
                'success': False,
                'output': '',
                'error': 'GCC compiler not found at C:\\ProgramData\\mingw64\\mingw64\\bin\\gcc.exe\nRun: choco install mingw -y',
                'exit_code': -1
            }
        
        try:
            # Create temporary C file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False, encoding='utf-8') as src_file:
                src_file.write(code)
                src_path = src_file.name
            
            print(f"🔧 Compiling C with: {compiler}")
            
            # Compile C code
            exe_path = src_path + '.exe'
            compile_process = subprocess.run(
                [compiler, src_path, '-o', exe_path],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if compile_process.returncode != 0:
                try:
                    os.unlink(src_path)
                except:
                    pass
                return {
                    'success': False,
                    'output': '',
                    'error': compile_process.stderr,
                    'exit_code': compile_process.returncode
                }
            
            print("✅ C compilation successful, executing...")
            
            # Execute the compiled program
            exec_process = subprocess.run(
                [exe_path],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            # Cleanup
            try:
                os.unlink(src_path)
                os.unlink(exe_path)
            except:
                pass
            
            return {
                'success': True,
                'output': exec_process.stdout,
                'error': exec_process.stderr,
                'exit_code': exec_process.returncode
            }
            
        except subprocess.TimeoutExpired:
            try:
                os.unlink(src_path)
                if 'exe_path' in locals():
                    os.unlink(exe_path)
            except:
                pass
            return {
                'success': False,
                'output': '',
                'error': 'Execution timeout',
                'exit_code': -1
            }
        except Exception as e:
            try:
                if 'src_path' in locals():
                    os.unlink(src_path)
                if 'exe_path' in locals():
                    os.unlink(exe_path)
            except:
                pass
            return {
                'success': False,
                'output': '',
                'error': f'C compilation error: {str(e)}',
                'exit_code': -1
            }
    
    def execute(self, code: str, input_data: str, timeout: int, memory_limit: int) -> Dict[str, Any]:
        return self.compile_code(code, input_data, timeout, memory_limit)

class CppLanguage(BaseLanguage):
    @property
    def name(self) -> str:
        return "C++"
    
    @property
    def extension(self) -> str:
        return ".cpp"
    
    def _find_compiler(self):
        """Find G++ compiler using known Chocolatey location"""
        # Known Chocolatey MinGW location
        known_paths = [
            r"C:\ProgramData\mingw64\mingw64\bin\g++.exe",
            r"C:\tools\mingw64\bin\g++.exe"
        ]
        
        for compiler_path in known_paths:
            if os.path.exists(compiler_path):
                print(f"🎯 Found G++ at: {compiler_path}")
                return compiler_path
        
        # Also try PATH
        try:
            subprocess.run(['g++', '--version'], capture_output=True, timeout=2)
            print("🎯 Found G++ in PATH")
            return 'g++'
        except:
            pass
        
        print("❌ G++ compiler not found")
        return None
    
    def compile_code(self, code: str, input_data: str, timeout: int, memory_limit: int) -> Dict[str, Any]:
        compiler = self._find_compiler()
        
        if not compiler:
            return {
                'success': False,
                'output': '',
                'error': 'G++ compiler not found at C:\\ProgramData\\mingw64\\mingw64\\bin\\g++.exe\nRun: choco install mingw -y',
                'exit_code': -1
            }
        
        try:
            # Create temporary C++ file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False, encoding='utf-8') as src_file:
                src_file.write(code)
                src_path = src_file.name
            
            print(f"🔧 Compiling C++ with: {compiler}")
            
            # Compile C++ code
            exe_path = src_path + '.exe'
            compile_process = subprocess.run(
                [compiler, src_path, '-o', exe_path],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if compile_process.returncode != 0:
                try:
                    os.unlink(src_path)
                except:
                    pass
                return {
                    'success': False,
                    'output': '',
                    'error': compile_process.stderr,
                    'exit_code': compile_process.returncode
                }
            
            print("✅ C++ compilation successful, executing...")
            
            # Execute the compiled program
            exec_process = subprocess.run(
                [exe_path],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            # Cleanup
            try:
                os.unlink(src_path)
                os.unlink(exe_path)
            except:
                pass
            
            return {
                'success': True,
                'output': exec_process.stdout,
                'error': exec_process.stderr,
                'exit_code': exec_process.returncode
            }
            
        except subprocess.TimeoutExpired:
            try:
                os.unlink(src_path)
                if 'exe_path' in locals():
                    os.unlink(exe_path)
            except:
                pass
            return {
                'success': False,
                'output': '',
                'error': 'Execution timeout',
                'exit_code': -1
            }
        except Exception as e:
            try:
                if 'src_path' in locals():
                    os.unlink(src_path)
                if 'exe_path' in locals():
                    os.unlink(exe_path)
            except:
                pass
            return {
                'success': False,
                'output': '',
                'error': f'C++ compilation error: {str(e)}',
                'exit_code': -1
            }
    
    def execute(self, code: str, input_data: str, timeout: int, memory_limit: int) -> Dict[str, Any]:
        return self.compile_code(code, input_data, timeout, memory_limit)