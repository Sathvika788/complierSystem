import asyncio
import redis
import json
from typing import Dict, Any

from src.core.compiler import compiler_manager
from src.database.redis_client import redis_client

class SubmissionExecutor:
    def __init__(self):
        self.redis_client = redis_client
    
    async def process_queue(self):
        """Continuously process submissions from the queue"""
        print("Worker started - waiting for submissions...")
        
        while True:
            try:
                # Blocking pop from queue
                submission_id = self.redis_client.brpop("submission_queue", timeout=0)[1]
                
                if submission_id:
                    await self.process_submission(submission_id)
                    
            except Exception as e:
                print(f"Error processing queue: {e}")
                await asyncio.sleep(1)
    
    async def process_submission(self, submission_id: str):
        """Process a single submission"""
        try:
            data = self.redis_client.get(f"submission:{submission_id}")
            if not data:
                print(f"Submission {submission_id} not found")
                return
            
            submission = json.loads(data)
            
            # Update status
            submission["status"] = "Processing"
            self.redis_client.setex(
                f"submission:{submission_id}", 
                3600, 
                json.dumps(submission)
            )
            
            # Execute code
            result = await compiler_manager.execute_code(
                source_code=submission["source_code"],
                language_id=submission["language_id"],
                stdin=submission["stdin"],
                cpu_time_limit=submission["cpu_time_limit"],
                memory_limit=submission["memory_limit"]
            )
            
            # Update with result
            submission.update(result)
            submission["status"] = "Completed"
            self.redis_client.setex(
                f"submission:{submission_id}", 
                3600, 
                json.dumps(submission)
            )
            
            print(f"Processed submission {submission_id} successfully")
            
        except Exception as e:
            print(f"Error processing submission {submission_id}: {e}")
            
            # Update with error
            error_data = {
                "status": "Error",
                "stderr": f"Execution failed: {str(e)}",
                "exit_code": 1
            }
            
            data = self.redis_client.get(f"submission:{submission_id}")
            if data:
                submission = json.loads(data)
                submission.update(error_data)
                self.redis_client.setex(
                    f"submission:{submission_id}", 
                    3600, 
                    json.dumps(submission)
                )

executor = SubmissionExecutor()