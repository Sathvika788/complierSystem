import os
from typing import Dict, Any

class Config:
    # API Settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # Redis Settings
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB = int(os.getenv("REDIS_DB", "0"))
    
    # Security Settings
    MAX_CPU_TIME = float(os.getenv("MAX_CPU_TIME", "30.0"))
    MAX_MEMORY = int(os.getenv("MAX_MEMORY", "512000"))  # KB
    MAX_PROCESSES = int(os.getenv("MAX_PROCESSES", "50"))
    
    # Execution Settings
    DEFAULT_TIMEOUT = float(os.getenv("DEFAULT_TIMEOUT", "5.0"))
    TEMP_DIR = os.getenv("TEMP_DIR", "/tmp/compiler")
    
    # Language Settings
    LANGUAGE_CONFIG: Dict[int, Dict[str, Any]] = {
        1: {"name": "C", "extension": ".c", "compile_cmd": "gcc {source} -o {executable}"},
        2: {"name": "C++", "extension": ".cpp", "compile_cmd": "g++ {source} -o {executable}"},
        3: {"name": "Python", "extension": ".py", "run_cmd": "python {source}"},
        4: {"name": "Java", "extension": ".java", "compile_cmd": "javac {source}", "run_cmd": "java {main_class}"},
        5: {"name": "JavaScript", "extension": ".js", "run_cmd": "node {source}"},
        6: {"name": "Go", "extension": ".go", "compile_cmd": "go build -o {executable} {source}"},
        7: {"name": "Rust", "extension": ".rs", "compile_cmd": "rustc -o {executable} {source}"},
        8: {"name": "SQL", "extension": ".sql", "run_cmd": "sqlite3"}
    }

config = Config()