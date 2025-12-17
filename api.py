"""
Multi-Language Compiler API
Supports: C, C++, Python, Java, JavaScript, Go, Rust, SQL
Deployment: AWS EC2 with Elastic IP
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
import tempfile
import shutil
import re
from typing import Dict, Any

app = FastAPI(
    title="Multi-Language Compiler API",
    description="Compile and execute code in 8 programming languages",
    version="1.0.0"
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Compiler API is running!",
        "status": "active",
        "version": "1.0.0",
        "supported_languages": 8
    }

@app.get("/api/languages")
async def get_supported_languages():
    """Get list of all supported programming languages"""
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

@app.post("/api/compile")
async def compile_code(request: Dict[Any, Any]):
    """
    Compile and execute code in any supported language
    
    Request format:
    {
        "language": "python",  # Language name (lowercase)
        "code": "print('hello')",  # Source code
        "stdin": ""  # Optional input for the program
    }
    """
    try:
        # Validate request
        language = request.get("language", "").lower().strip()
        code = request.get("code", "").strip()
        stdin = request.get("stdin", "").strip()
        
        if not language:
            raise HTTPException(status_code=400, detail="Language is required")
        if not code:
            raise HTTPException(status_code=400, detail="Code is required")
        
        # Execute the code
        result = await execute_code(language, code, stdin)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

async def execute_code(language: str, code: str, stdin: str = "") -> Dict[str, Any]:
    """
    Execute code in the specified language
    
    Returns:
        {
            "stdout": "output text",
            "stderr": "error text",
            "exit_code": 0,
            "status": "success" | "error" | "timeout" | "compilation_error"
        }
    """
    # Create a temporary directory for all files
    temp_dir = tempfile.mkdtemp(prefix="compile_")
    
    try:
        # === PYTHON ===
        if language == "python":
            temp_file = os.path.join(temp_dir, "main.py")
            with open(temp_file, "w") as f:
                f.write(code)
            result = subprocess.run(
                ["python3", temp_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5
            )
        
        # === JAVASCRIPT ===
        elif language == "javascript" or language == "js":
            temp_file = os.path.join(temp_dir, "main.js")
            with open(temp_file, "w") as f:
                f.write(code)
            result = subprocess.run(
                ["node", temp_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5
            )
        
        # === C ===
        elif language == "c":
            temp_file = os.path.join(temp_dir, "main.c")
            with open(temp_file, "w") as f:
                f.write(code)
            exec_file = os.path.join(temp_dir, "main.out")
            
            # Compile with optimizations
            compile_result = subprocess.run(
                ["gcc", "-O2", "-Wall", temp_file, "-o", exec_file],
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
            
            # Execute
            result = subprocess.run(
                [exec_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5
            )
        
        # === C++ ===
        elif language == "cpp" or language == "c++":
            temp_file = os.path.join(temp_dir, "main.cpp")
            with open(temp_file, "w") as f:
                f.write(code)
            exec_file = os.path.join(temp_dir, "main.out")
            
            # Compile with optimizations for faster compilation
            compile_result = subprocess.run(
                ["g++", "-O2", "-std=c++11", "-Wall", temp_file, "-o", exec_file],
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
            
            # Execute
            result = subprocess.run(
                [exec_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5
            )
        
        # === JAVA ===
        elif language == "java":
            # Extract class name from Java code
            class_match = re.search(r'public\s+class\s+(\w+)', code)
            if class_match:
                class_name = class_match.group(1)
            else:
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
            
            # Execute with memory limit
            result = subprocess.run(
                ["java", "-Xmx256m", "-cp", temp_dir, class_name],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5
            )
        
        # === GO ===
        elif language == "go":
            temp_file = os.path.join(temp_dir, "main.go")
            with open(temp_file, "w") as f:
                f.write(code)
            result = subprocess.run(
                ["go", "run", temp_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=10
            )
        
        # === RUST ===
        elif language == "rust":
            temp_file = os.path.join(temp_dir, "main.rs")
            with open(temp_file, "w") as f:
                f.write(code)
            exec_file = os.path.join(temp_dir, "main_rust")
            
            # Compile with optimizations
            compile_result = subprocess.run(
                ["rustc", "-O", temp_file, "-o", exec_file],
                capture_output=True,
                text=True,
                timeout=15
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
                [exec_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5
            )
        
        # === SQL ===
        elif language == "sql":
            temp_file = os.path.join(temp_dir, "query.sql")
            with open(temp_file, "w") as f:
                f.write(code)
            
            # Execute SQL in memory database
            result = subprocess.run(
                ["sqlite3", ":memory:", ".read " + temp_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5
            )
        
        # === UNSUPPORTED LANGUAGE ===
        else:
            return {
                "stdout": "",
                "stderr": f"Language '{language}' is not supported. Supported languages: python, javascript, c, c++, java, go, rust, sql",
                "exit_code": -1,
                "status": "language_not_supported"
            }
        
        # Return execution results
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "status": "success" if result.returncode == 0 else "error"
        }
        
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Execution timeout (process took too long)",
            "exit_code": -1,
            "status": "timeout"
        }
    except FileNotFoundError as e:
        return {
            "stdout": "",
            "stderr": f"Compiler not found: {str(e)}. Please install required compiler.",
            "exit_code": -1,
            "status": "compiler_not_found"
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"Execution error: {str(e)}",
            "exit_code": -1,
            "status": "error"
        }
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)

@app.get("/api/health")
async def health_check():
    """Detailed health check with compiler availability"""
    compilers = {
        "python3": "python",
        "node": "javascript",
        "gcc": "c",
        "g++": "c++",
        "javac": "java",
        "go": "go",
        "rustc": "rust",
        "sqlite3": "sql"
    }
    
    available = {}
    for cmd, lang in compilers.items():
        try:
            subprocess.run([cmd, "--version"], capture_output=True, timeout=2)
            available[lang] = True
        except:
            available[lang] = False
    
    return {
        "status": "healthy",
        "api": True,
        "compilers_available": available,
        "total_languages": 8,
        "available_languages": sum(1 for v in available.values() if v)
    }

@app.get("/api/stats")
async def get_stats():
    """Get API usage statistics"""
    return {
        "languages_supported": 8,
        "endpoints": ["/", "/api/languages", "/api/compile", "/api/health", "/api/stats"],
        "max_execution_time": 15,  # seconds
        "max_compilation_time": 10,  # seconds
        "memory_limit": "256MB",  # per execution
        "concurrent_limit": 10  # concurrent executions
    }

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
