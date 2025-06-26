import threading
import time
from typing import Optional, List
import tkinter as tk
from tkinter import ttk
from colorama import Fore, Style , init
init(autoreset=True)  # Automatically reset color after each print

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
    """Core Queue Management Module + Module 2: Priority Aging"""
    
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.queue = [None] * capacity  # Circular queue array
        self.front = 0  # Points to front of queue
        self.rear = 0   # Points to next insertion position
        self.size = 0   # Current number of jobs
        self.lock = threading.RLock()  # Thread safety

        # Module 2: Priority Aging
        self.interval = 5  
        # Module 3: Job Expiry
        self.expiry_threshold = 10

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

  
    # MODULE 2: Priority Aging
 
    def apply_priority_aging(self):
        """Increase job priority over time and reorder"""
        with self.lock:
            now = time.time()
            jobs = self.get_all_jobs()

            for job in jobs:
                job.waiting_time = int(now - job.submit_time)
                if job.waiting_time >= self.interval and job.priority < 10:
                    job.priority += 1
                    job.submit_time = now  # reset for next interval
                    print(f"[AGING] Job {job.job_id} aged to priority {job.priority}")

            self._reorder_jobs(jobs)

    def _reorder_jobs(self, jobs: List[Job]):
        """Sort jobs by priority and waiting time (descending)"""
        jobs.sort(key=lambda j: (-j.priority, -j.waiting_time))

        for i in range(self.capacity):
            self.queue[i] = None

        self.front = 0
        self.rear = 0
        self.size = 0

        for job in jobs:
            self.queue[self.rear] = job
            self.rear = (self.rear + 1) % self.capacity
            self.size += 1


    # MODULE 3: Job Expiry

    def remove_expired_jobs(self):
        """Remove jobs that have exceeded expiry time"""
        with self.lock:
            now = time.time()
            jobs = self.get_all_jobs()

            valid_jobs = []
            expired_jobs = []

            for job in jobs:
                job.waiting_time = int(now - job.submit_time)
                if job.waiting_time >= self.expiry_threshold:
                    expired_jobs.append(job)
                else:
                    valid_jobs.append(job)

            for job in expired_jobs:
                print(f"[EXPIRED] Job {job.job_id} removed (waited {job.waiting_time}s)")

            self._reorder_jobs(valid_jobs)
    def show_gui(self):
        Window = tk.Tk()
        Window.title("Print Queue Visualization.")
    
        columns = ("Position", "User ID", "Job ID", "Priority", "Wait Time")
        tree = ttk.Treeview(Window, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
    
        for i, job in enumerate(self.get_all_jobs(), start=1):  # safer than using self.queue directly
            tree.insert("", "end", values=(i, job.user_id, job.job_id, job.priority, job.waiting_time))

        tree.pack(padx=10, pady=10)
        Window.mainloop()


    def show_status(self):
        jobs = self.get_all_jobs()
        if not jobs:
            print(Fore.RED + "\n--- Print Queue is currently empty ---\n")
            return

        print(Fore.CYAN + "\n--- Current Print Queue Status ---")
        print(Fore.YELLOW + f"{'Position':<10} {'User':<10} {'Job ID':<10} {'Priority':<10} {'Wait Time':<10}")
        print(Fore.YELLOW + "-" * 55)

        for index, job in enumerate(jobs, start=1):
            print(Fore.GREEN + f"{index:<10} {job.user_id:<10} {job.job_id:<10} {job.priority:<10} {job.waiting_time:<10}")
    
        print(Fore.YELLOW + "-" * 55 + "\n")

        
