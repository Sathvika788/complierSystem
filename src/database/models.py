from typing import Dict, Any, Optional
from datetime import datetime

class Submission:
    def __init__(self, submission_id: str, source_code: str, language_id: int,
                 stdin: str = "", expected_output: Optional[str] = None,
                 cpu_time_limit: float = 5.0, memory_limit: int = 256000):
        self.submission_id = submission_id
        self.source_code = source_code
        self.language_id = language_id
        self.stdin = stdin
        self.expected_output = expected_output
        self.cpu_time_limit = cpu_time_limit
        self.memory_limit = memory_limit
        self.status = "In Queue"
        self.stdout = ""
        self.stderr = ""
        self.exit_code = 0
        self.execution_time = 0.0
        self.created_at = datetime.utcnow()
        self.completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "submission_id": self.submission_id,
            "source_code": self.source_code,
            "language_id": self.language_id,
            "stdin": self.stdin,
            "expected_output": self.expected_output,
            "cpu_time_limit": self.cpu_time_limit,
            "memory_limit": self.memory_limit,
            "status": self.status,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "exit_code": self.exit_code,
            "execution_time": self.execution_time,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Submission':
        submission = cls(
            submission_id=data["submission_id"],
            source_code=data["source_code"],
            language_id=data["language_id"],
            stdin=data.get("stdin", ""),
            expected_output=data.get("expected_output"),
            cpu_time_limit=data.get("cpu_time_limit", 5.0),
            memory_limit=data.get("memory_limit", 256000)
        )
        
        submission.status = data.get("status", "In Queue")
        submission.stdout = data.get("stdout", "")
        submission.stderr = data.get("stderr", "")
        submission.exit_code = data.get("exit_code", 0)
        submission.execution_time = data.get("execution_time", 0.0)
        
        if "created_at" in data and data["created_at"]:
            submission.created_at = datetime.fromisoformat(data["created_at"])
        
        if "completed_at" in data and data["completed_at"]:
            submission.completed_at = datetime.fromisoformat(data["completed_at"])
        
        return submission