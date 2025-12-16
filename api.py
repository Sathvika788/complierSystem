from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
import tempfile
import shutil
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
        language_id = request.get("language_id")
        source_code = request.get("source_code")
        stdin = request.get("stdin", "")
        
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
        
        result = await execute_code(language, source_code, stdin)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def execute_code(language: str, code: str, stdin: str = ""):
    """EXECUTE CODE FOR ALL 8 LANGUAGES"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=get_file_extension(language)) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        if language == "python":
            result = subprocess.run(
                ["python3", temp_file],
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
            
            result = subprocess.run(
                [exec_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5
            )
            if os.path.exists(exec_file):
                os.unlink(exec_file)
                
        elif language == "cpp":
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
            
            result = subprocess.run(
                [exec_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5
            )
            if os.path.exists(exec_file):
                os.unlink(exec_file)
                
        elif language == "java":
            # Java needs the class name to match file name
            class_name = "Main"
            class_file = f"{class_name}.class"
            
            compile_result = subprocess.run(
                ["javac", temp_file],
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
            
            # Run from the temp directory
            result = subprocess.run(
                ["java", "-cp", os.path.dirname(temp_file), class_name],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Clean up class file
            class_path = os.path.join(os.path.dirname(temp_file), class_file)
            if os.path.exists(class_path):
                os.unlink(class_path)
                
        elif language == "go":
            # Go run compiles and executes in one step
            result = subprocess.run(
                ["go", "run", temp_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=10
            )
            
        elif language == "rust":
            # Rust needs proper cargo project
            rust_dir = tempfile.mkdtemp()
            src_dir = os.path.join(rust_dir, "src")
            os.makedirs(src_dir)
            
            main_rs = os.path.join(src_dir, "main.rs")
            with open(main_rs, 'w') as f:
                f.write(code)
            
            cargo_toml = os.path.join(rust_dir, "Cargo.toml")
            with open(cargo_toml, 'w') as f:
                f.write('[package]\nname = "temp_rust"\nversion = "0.1.0"\nedition = "2021"\n\n[dependencies]\n')
            
            result = subprocess.run(
                ["cargo", "run", "--manifest-path", cargo_toml, "--quiet"],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=15
            )
            
            # Clean up
            shutil.rmtree(rust_dir)
            
        elif language == "sql":
            # SQL execution with sqlite3
            result = subprocess.run(
                ["sqlite3", ":memory:"],
                input=code,
                capture_output=True,
                text=True,
                timeout=5
            )
            
        else:
            return {
                "stdout": "",
                "stderr": f"Language {language} not supported",
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
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "exit_code": -1, "status": "error"}
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def get_file_extension(language: str) -> str:
    extensions = {
        "python": ".py",
        "javascript": ".js", 
        "java": ".java",
        "c": ".c",
        "cpp": ".cpp",
        "go": ".go",
        "rust": ".rs",
        "sql": ".sql"
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
            {"id": 7, "name": "Rust"},
            {"id": 8, "name": "SQL"}
        ]
    }
