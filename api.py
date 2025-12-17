from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
import tempfile
import shutil
import re
from typing import Dict, Any

app = FastAPI(title="Multi-Language Compiler API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

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
            raise HTTPException(status_code=400, detail="Language and code required")
        result = await execute_code(language, code, stdin)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def execute_code(language: str, code: str, stdin: str = ""):
    # Create a temporary directory for all files (better isolation)
    temp_dir = tempfile.mkdtemp()
    
    try:
        if language == "python":
            temp_file = os.path.join(temp_dir, "main.py")
            with open(temp_file, "w") as f:
                f.write(code)
            result = subprocess.run(["python3", temp_file], input=stdin, capture_output=True, text=True, timeout=5)
            
        elif language == "javascript":
            temp_file = os.path.join(temp_dir, "main.js")
            with open(temp_file, "w") as f:
                f.write(code)
            result = subprocess.run(["node", temp_file], input=stdin, capture_output=True, text=True, timeout=5)
            
        elif language == "c":
            temp_file = os.path.join(temp_dir, "main.c")
            with open(temp_file, "w") as f:
                f.write(code)
            exec_file = os.path.join(temp_dir, "main.out")
            compile_result = subprocess.run(["gcc", temp_file, "-o", exec_file], capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return {"stdout": "", "stderr": compile_result.stderr, "exit_code": compile_result.returncode, "status": "compilation_error"}
            result = subprocess.run([exec_file], input=stdin, capture_output=True, text=True, timeout=5)
            
        elif language == "cpp":
            temp_file = os.path.join(temp_dir, "main.cpp")
            with open(temp_file, "w") as f:
                f.write(code)
            exec_file = os.path.join(temp_dir, "main.out")
            compile_result = subprocess.run(["g++", temp_file, "-o", exec_file], capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return {"stdout": "", "stderr": compile_result.stderr, "exit_code": compile_result.returncode, "status": "compilation_error"}
            result = subprocess.run([exec_file], input=stdin, capture_output=True, text=True, timeout=5)
            
        elif language == "java":
            # Extract class name from Java code
            # Look for public class first
            class_match = re.search(r'public\s+class\s+(\w+)', code)
            if class_match:
                class_name = class_match.group(1)
            else:
                # Look for any class (non-public)
                class_match = re.search(r'class\s+(\w+)', code)
                class_name = class_match.group(1) if class_match else "Main"
            
            # Write Java file with correct name
            java_file = os.path.join(temp_dir, f"{class_name}.java")
            with open(java_file, "w") as f:
                f.write(code)
            
            # Compile
            compile_result = subprocess.run(
                ["javac", java_file],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=temp_dir
            )
            
            if compile_result.returncode != 0:
                return {
                    "stdout": "", 
                    "stderr": compile_result.stderr, 
                    "exit_code": compile_result.returncode, 
                    "status": "compilation_error"
                }
            
            # Execute
            result = subprocess.run(
                ["java", "-cp", temp_dir, class_name],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5
            )
            
        elif language == "go":
            temp_file = os.path.join(temp_dir, "main.go")
            with open(temp_file, "w") as f:
                f.write(code)
            result = subprocess.run(["go", "run", temp_file], input=stdin, capture_output=True, text=True, timeout=10)
            
        elif language == "rust":
            temp_file = os.path.join(temp_dir, "main.rs")
            with open(temp_file, "w") as f:
                f.write(code)
            exec_file = os.path.join(temp_dir, "main")
            compile_result = subprocess.run(["rustc", temp_file, "-o", exec_file], capture_output=True, text=True, timeout=15)
            if compile_result.returncode != 0:
                return {"stdout": "", "stderr": compile_result.stderr, "exit_code": compile_result.returncode, "status": "compilation_error"}
            result = subprocess.run([exec_file], input=stdin, capture_output=True, text=True, timeout=5)
            
        elif language == "sql":
            temp_file = os.path.join(temp_dir, "query.sql")
            with open(temp_file, "w") as f:
                f.write(code)
            result = subprocess.run(["sqlite3", ":memory:", ".read " + temp_file], input=stdin, capture_output=True, text=True, timeout=5)
            
        else:
            return {"stdout": "", "stderr": f"Language {language} not supported", "exit_code": -1, "status": "language_not_supported"}

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "status": "success" if result.returncode == 0 else "error"
        }
        
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Execution timeout", "exit_code": -1, "status": "timeout"}
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "exit_code": -1, "status": "error"}
    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)

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
            {"id": 7, "name": "Rust"},
            {"id": 8, "name": "SQL"}
        ]
    }
