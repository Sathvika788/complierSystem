from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
import tempfile
import uuid
from typing import Dict, Any

app = FastAPI(title="Multi-Language Compiler API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Compiler API is running!", "status": "active"}

@app.post("/api/compile")
async def compile_code(request: Dict[Any, Any]):
    try:
        language = request.get("language")
        code = request.get("code")
        stdin = request.get("stdin", "")
        
        if not language or not code:
            raise HTTPException(status_code=400, detail="Language and code are required")
        
        # ACTUALLY EXECUTE THE CODE
        result = await execute_code(language, code, stdin)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/submissions")
async def submissions_v1(request: dict):
    """
    Compatibility endpoint for Judge0-style requests
    """
    try:
        # Convert Judge0 format to your format
        language_id = request.get("language_id")
        source_code = request.get("source_code")
        stdin = request.get("stdin", "")
        
        # Map language_id to language name
        language_map = {
            1: "c",      # C
            2: "cpp",    # C++
            3: "python", # Python
            4: "java",   # Java
            5: "javascript", # JavaScript
            6: "go",     # Go
            7: "rust",   # Rust
            8: "sql"     # SQL
        }
        
        language = language_map.get(language_id)
        if not language:
            raise HTTPException(status_code=400, detail="Unsupported language_id")
        
        # Call your existing compile logic
        result = await execute_code(language, source_code, stdin)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def execute_code(language: str, code: str, stdin: str = ""):
    """ACTUALLY EXECUTE THE CODE - THIS IS THE REAL COMPILATION LOGIC"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=get_file_extension(language)) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        if language == "python":
            result = subprocess.run(
                ["python", temp_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5
            )
        elif language == "javascript":
            result = subprocess.run(
                ["node", temp_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5
            )
        elif language == "c":
            # Compile C code
            exec_file = temp_file + ".exe"
            compile_result = subprocess.run(
                ["gcc", temp_file, "-o", exec_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            if compile_result.returncode != 0:
                return {
                    "stdout": "",
                    "stderr": compile_result.stderr,
                    "exit_code": compile_result.returncode,
                    "status": "compilation_error"
                }
            
            # Execute compiled C code
            result = subprocess.run(
                [exec_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5
            )
            os.unlink(exec_file)
        elif language == "cpp":
            # Compile C++ code
            exec_file = temp_file + ".exe"
            compile_result = subprocess.run(
                ["g++", temp_file, "-o", exec_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            if compile_result.returncode != 0:
                return {
                    "stdout": "",
                    "stderr": compile_result.stderr,
                    "exit_code": compile_result.returncode,
                    "status": "compilation_error"
                }
            
            # Execute compiled C++ code
            result = subprocess.run(
                [exec_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5
            )
            os.unlink(exec_file)
        # Add more languages as needed...
        else:
            return {
                "stdout": "",
                "stderr": f"Language {language} not implemented yet",
                "exit_code": -1,
                "status": "language_not_supported"
            }
        
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "status": "success" if result.returncode == 0 else "error"
        }
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Execution timeout", "exit_code": -1, "status": "timeout"}
    finally:
        os.unlink(temp_file)

def get_file_extension(language: str) -> str:
    extensions = {
        "python": ".py",
        "javascript": ".js", 
        "java": ".java",
        "c": ".c",
        "cpp": ".cpp",
        "go": ".go",
        "rust": ".rs"
    }
    return extensions.get(language, ".txt")

@app.get("/api/languages")
async def get_supported_languages():
    return {
        "languages": [
            {"id": 1, "name": "C"},
            {"id": 2, "name": "C++"},
            {"id": 3, "name": "Python"},
            {"id": 4, "name": "Java"},
            {"id": 5, "name": "JavaScript"},
            {"id": 6, "name": "Go"},
            {"id": 7, "name": "Rust"}
        ]
    }