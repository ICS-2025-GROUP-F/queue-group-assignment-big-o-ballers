import threading
import time
from typing import Optional, List, Dict, Any

class Job:
    """Represents a print job with metadata"""
    def __init__(self, user_id: str, job_id: str, priority: int = 1):
        self.user_id = user_id
        self.job_id = job_id
        self.priority = priority
        self.submit_time = time.time()
        self.waiting_time = 0
    
    def __str__(self):
        return f"Job({self.user_id}-{self.job_id}, P:{self.priority}, W:{self.waiting_time}s)"

class PrintQueueManager:
    """Core Queue Management Module - Circular Queue Implementation"""
    
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.queue = [None] * capacity  # Circular queue array
        self.front = 0  # Points to front of queue
        self.rear = 0   # Points to next insertion position
        self.size = 0   # Current number of jobs
        self.lock = threading.RLock()  # Thread safety
    
    def enqueue_job(self, user_id: str, job_id: str, priority: int = 1) -> bool:
        """Add a new job to the queue"""
        with self.lock:
            if self.size >= self.capacity:
                return False
            
            job = Job(user_id, job_id, priority)
            self.queue[self.rear] = job
            self.rear = (self.rear + 1) % self.capacity
            self.size += 1
            return True
    
    def dequeue_job(self) -> Optional[Job]:
        """Remove and return job from front of queue"""
        with self.lock:
            if self.size == 0:
                return None
            
            job = self.queue[self.front]
            self.queue[self.front] = None
            self.front = (self.front + 1) % self.capacity
            self.size -= 1
            return job
    
    def show_status(self) -> None:
        """Display current queue status"""
        with self.lock:
            print(f"\nQueue Status: {self.size}/{self.capacity} jobs")
            if self.size == 0:
                print("Queue is empty")
                return
            
            print("Jobs in queue:")
            current = self.front
            for i in range(self.size):
                job = self.queue[current]
                print(f"{i+1}. {job}")
                current = (current + 1) % self.capacity
            print()
    
    # Helper methods for other modules
    def get_all_jobs(self) -> List[Job]:
        """Get all jobs for other modules to access"""
        with self.lock:
            jobs = []
            current = self.front
            for _ in range(self.size):
                jobs.append(self.queue[current])
                current = (current + 1) % self.capacity
            return jobs
    
    def is_empty(self) -> bool:
        return self.size == 0
    
    def is_full(self) -> bool:
        return self.size >= self.capacity
