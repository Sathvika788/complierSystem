from abc import ABC, abstractmethod
import asyncio
import os
from typing import Dict, Any
import subprocess

class BaseLanguage(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def extension(self) -> str:
        pass
    
    @abstractmethod
    async def execute(self, source_code: str, stdin: str, 
                     temp_dir: str, cpu_time_limit: float,
                     memory_limit: int) -> Dict[str, Any]:
        pass
    
    async def run_command(self, command: str, stdin: str = "", 
                         timeout: float = 5.0, cwd: str = None) -> Dict[str, Any]:
        """Generic command execution with timeout"""
        try:
            process = await asyncio.create_subprocess_exec(
                *command.split(),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(input=stdin.encode()),
                timeout=timeout
            )
            
            return {
                "stdout": stdout.decode().strip(),
                "stderr": stderr.decode().strip(),
                "exit_code": process.returncode,
                "timeout": False
            }
            
        except asyncio.TimeoutError:
            return {
                "stdout": "",
                "stderr": f"Execution timed out after {timeout} seconds",
                "exit_code": -1,
                "timeout": True
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": f"Execution failed: {str(e)}",
                "exit_code": -1,
                "timeout": False
            }