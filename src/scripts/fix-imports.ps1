Write-Host "Fixing import errors..." -ForegroundColor Green

# Create missing language files
$base_language = @"
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
                \"stdout\": stdout.decode().strip(),
                \"stderr\": stderr.decode().strip(),
                \"exit_code\": process.returncode,
                \"timeout\": False
            }
            
        except asyncio.TimeoutError:
            return {
                \"stdout\": \"\",
                \"stderr\": f\"Execution timed out after {timeout} seconds\",
                \"exit_code\": -1,
                \"timeout\": True
            }
        except Exception as e:
            return {
                \"stdout\": \"\",
                \"stderr\": f\"Execution failed: {str(e)}\",
                \"exit_code\": -1,
                \"timeout\": False
            }
"@

Set-Content -Path "src/languages/base.py" -Value $base_language

Write-Host "✅ Fixed base language class" -ForegroundColor Green

# Fix the typo in main.py
$main_content = Get-Content "src/api/main.py" -Raw
$fixed_content = $main_content -replace "from src.core.complier import", "from src.core.compiler import"
Set-Content -Path "src/api/main.py" -Value $fixed_content

Write-Host "✅ Fixed typo in main.py" -ForegroundColor Green
Write-Host "🎉 Now try running: python -m uvicorn src.api.main:app --reload" -ForegroundColor Green