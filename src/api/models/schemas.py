from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class SubmissionBase(BaseModel):
    source_code: str
    language_id: int
    stdin: Optional[str] = ""
    expected_output: Optional[str] = None
    cpu_time_limit: Optional[float] = 5.0
    memory_limit: Optional[int] = 256000
    compiler_options: Optional[str] = None

class SubmissionCreate(SubmissionBase):
    pass

class SubmissionResponse(SubmissionBase):
    submission_id: str
    status: str
    stdout: Optional[str] = ""
    stderr: Optional[str] = ""
    exit_code: Optional[int] = 0
    execution_time: Optional[float] = 0.0
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True