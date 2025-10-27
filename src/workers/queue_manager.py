import asyncio
from src.workers.executor import executor

async def start_worker():
    """Start the worker to process submissions"""
    print("Starting submission worker...")
    await executor.process_queue()

if __name__ == "__main__":
    asyncio.run(start_worker())