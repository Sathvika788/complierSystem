# This is the complete api.py code - save it on your Windows machine
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
import tempfile
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
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=get_file_extension(language)) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        if language == "python":
            result = subprocess.run(["python3", temp_file], input=stdin, capture_output=True, text=True, timeout=5)
        elif language == "javascript":
            result = subprocess.run(["node", temp_file], input=stdin, capture_output=True, text=True, timeout=5)
        elif language == "c":
            exec_file = temp_file + ".out"
            compile_result = subprocess.run(["gcc", temp_file, "-o", exec_file], capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return {"stdout": "", "stderr": compile_result.stderr, "exit_code": compile_result.returncode, "status": "compilation_error"}
            result = subprocess.run([exec_file], input=stdin, capture_output=True, text=True, timeout=5)
            if os.path.exists(exec_file): os.unlink(exec_file)
        elif language == "cpp":
            exec_file = temp_file + ".out"
            compile_result = subprocess.run(["g++", temp_file, "-o", exec_file], capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return {"stdout": "", "stderr": compile_result.stderr, "exit_code": compile_result.returncode, "status": "compilation_error"}
            result = subprocess.run([exec_file], input=stdin, capture_output=True, text=True, timeout=5)
            if os.path.exists(exec_file): os.unlink(exec_file)
        elif language == "java":
            class_name = "Main"
            compile_result = subprocess.run(["javac", "-d", "/tmp", temp_file], capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return {"stdout": "", "stderr": compile_result.stderr, "exit_code": compile_result.returncode, "status": "compilation_error"}
            result = subprocess.run(["java", "-cp", "/tmp", class_name], input=stdin, capture_output=True, text=True, timeout=5)
            os.system("rm -f /tmp/Main.class 2>/dev/null")
        elif language == "go":
            result = subprocess.run(["go", "run", temp_file], input=stdin, capture_output=True, text=True, timeout=10)
        elif language == "rust":
            exec_file = temp_file + ".out"
            compile_result = subprocess.run(["rustc", temp_file, "-o", exec_file], capture_output=True, text=True, timeout=15)
            if compile_result.returncode != 0:
                return {"stdout": "", "stderr": compile_result.stderr, "exit_code": compile_result.returncode, "status": "compilation_error"}
            result = subprocess.run([exec_file], input=stdin, capture_output=True, text=True, timeout=5)
            if os.path.exists(exec_file): os.unlink(exec_file)
        elif language == "sql":
            result = subprocess.run(["sqlite3", ":memory:"], input=code, capture_output=True, text=True, timeout=5)
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
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def get_file_extension(language: str) -> str:
    extensions = {
        "python": ".py", "javascript": ".js", "java": ".java",
        "c": ".c", "cpp": ".cpp", "go": ".go", "rust": ".rs", "sql": ".sql"
    }
    return extensions.get(language, ".txt")
