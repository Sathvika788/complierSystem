from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
import json
from datetime import datetime

from src.database.redis_client import redis_client
from src.core.compiler import compiler_manager
from typing import Dict, Any
import asyncio

router = APIRouter(prefix="/submissions", tags=["submissions"])

class SubmissionRequest(BaseModel):
    source_code: str
    language_id: int
    stdin: Optional[str] = ""
    expected_output: Optional[str] = None
    cpu_time_limit: Optional[float] = 5.0
    memory_limit: Optional[int] = 256000

class SubmissionResponse(BaseModel):
    submission_id: str
    status: str
    message: Optional[str] = None

# Simple in-memory storage for submissions
submissions_db = {}

@router.post("", response_model=SubmissionResponse)
async def create_submission(request: SubmissionRequest, background_tasks: BackgroundTasks):
    submission_id = str(uuid.uuid4())
    
    # Store submission in memory
    submission_data = {
        **request.dict(),
        "submission_id": submission_id,
        "status": "In Queue",
        "created_at": datetime.utcnow().isoformat()
    }
    
    submissions_db[submission_id] = submission_data
    
    # Process immediately
    background_tasks.add_task(process_submission, submission_id)
    
    return SubmissionResponse(
        submission_id=submission_id,
        status="In Queue",
        message="Submission queued for execution"
    )

@router.get("/{submission_id}")
async def get_submission(submission_id: str):
    if submission_id not in submissions_db:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    return submissions_db[submission_id]

async def process_submission(submission_id: str):
    """Process submission immediately"""
    if submission_id not in submissions_db:
        return
    
    submission = submissions_db[submission_id]
    
    try:
        # Update status
        submission["status"] = "Processing"
        
        # Execute code directly - FIXED: Added missing closing parenthesis
        result = await asyncio.to_thread(
            compiler_manager.execute_code,
            source_code=submission["source_code"],
            language_id=submission["language_id"],
            stdin=submission["stdin"],
            cpu_time_limit=submission["cpu_time_limit"],
            memory_limit=submission["memory_limit"]
        )
        
        # Update with result
        submission.update(result)
        submission["status"] = "Completed"
        submission["completed_at"] = datetime.utcnow().isoformat()
        
    except Exception as e:
        # Update with error
        submission.update({
            "status": "Error",
            "stderr": f"Execution failed: {str(e)}",
            "exit_code": 1,
            "execution_time": 0.0
        })