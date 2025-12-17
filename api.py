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

@app.get("/api/health")
async def health_check():
    """Check compiler availability and API health"""
    compilers = {
        "python": "python3",
        "javascript": "node",
        "c": "gcc",
        "c++": "g++",
        "java": "javac",
        "go": "go",
        "rust": "rustc",
        "sql": "sqlite3"
    }
    
    compilers_available = {}
    for lang, cmd in compilers.items():
        compilers_available[lang] = shutil.which(cmd) is not None
    
    available_count = sum(compilers_available.values())
    
    return {
        "status": "healthy",
        "api": True,
        "compilers_available": compilers_available,
        "total_languages": len(compilers),
        "available_languages": available_count
    }

@app.get("/api/test-compiler/{language}")
async def test_compiler(language: str):
    """Test if a specific compiler works"""
    test_codes = {
        "python": "print('Python: OK')",
        "javascript": "console.log('JavaScript: OK')",
        "c": "#include <stdio.h>\nint main() { printf(\"C: OK\\n\"); return 0; }",
        "c++": "#include <iostream>\nusing namespace std;\nint main() { cout << \"C++: OK\" << endl; return 0; }",
        "java": "public class Test { public static void main(String[] args) { System.out.println(\"Java: OK\"); } }",
        "go": "package main\nimport \"fmt\"\nfunc main() { fmt.Println(\"Go: OK\") }",
        "rust": "fn main() { println!(\"Rust: OK\"); }",
        "sql": "SELECT 'SQL: OK';"
    }
    
    if language not in test_codes:
        raise HTTPException(status_code=400, detail="Language not supported")
    
    # Use the existing compile endpoint logic
    result = await execute_code(language, test_codes[language])
    
    return {
        "language": language,
        "test_code": test_codes[language],
        "result": result
    }

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

@app.get("/api/stats")
async def get_stats():
    """Get API statistics and system info"""
    import sys
    import platform
    
    # Get Python info
    python_version = sys.version
    
    # Get system info
    system_info = {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }
    
    # Get compiler availability
    health = await health_check()
    
    return {
        "api": "Multi-Language Compiler API",
        "version": "1.0.0",
        "python_version": python_version,
        "system_info": system_info,
        "compilers": health["compilers_available"],
        "available_languages": health["available_languages"],
        "total_languages": health["total_languages"],
        "timestamp": __import__("datetime").datetime.now().isoformat()
    }
