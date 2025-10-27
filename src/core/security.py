import psutil
import os
import signal

class SecurityManager:
    def set_memory_limit(self, memory_mb):
        """Set memory limit using psutil (cross-platform)"""
        try:
            process = psutil.Process()
            process.memory_limit(memory_mb * 1024 * 1024)  # Convert to bytes
        except AttributeError:
            # memory_limit might not be available on all platforms
            print(f"Memory limiting not supported on this platform. Requested: {memory_mb}MB")
    
    def set_time_limit(self, timeout_seconds):
        """Set time limit using signal (cross-platform)"""
        def timeout_handler(signum, frame):
            raise TimeoutError("Execution timed out")
        
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout_seconds)