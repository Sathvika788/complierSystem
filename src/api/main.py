from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, List
import uuid
import json
from datetime import datetime

from src.core.compiler import CompilerManager
from src.database.redis_client import redis_client
from src.api.routes import submissions, languages

app = FastAPI(
    title="Multi-Language Compiler API",
    description="Judge0-like compiler supporting 10+ languages including SQL",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(submissions.router, prefix="/api/v1")
app.include_router(languages.router, prefix="/api/v1")

# Global compiler manager
compiler_manager = CompilerManager()

@app.get("/")
async def root():
    return {"message": "Multi-Language Compiler API", "status": "active"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "supported_languages": len(compiler_manager.get_supported_languages())
    }
    # Add this at the end of src/api/main.py if missing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)