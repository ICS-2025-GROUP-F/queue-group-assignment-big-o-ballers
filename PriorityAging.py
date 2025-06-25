import time
from Job import PrintQueueManager

class PriorityAndAgingSystem:
    """
    Module 2: Handles priority-based ordering and aging of print jobs.
    """
    def __init__(self, queue_manager: PrintQueueManager, aging_interval: int = 10):
        
        self.queue_manager = queue_manager
        self.aging_interval = aging_interval  

    def apply_priority_aging(self):
       
        with self.queue_manager.lock:
            current_time = time.time()
            jobs = self.queue_manager.get_all_jobs()

            for job in jobs:
                job.waiting_time = int(current_time - job.submit_time)

                if job.waiting_time >= self.aging_interval and job.priority < 10:
                    job.priority += 1
                    job.submit_time = current_time  # Reset timer
                    print(f"[AGING] Job {job.job_id} priority increased to {job.priority}")

            self._reorder_queue(jobs)

    def _reorder_queue(self, jobs):
       
        jobs.sort(key=lambda j: (-j.priority, -j.waiting_time))

        # Clear the queue
        for i in range(self.queue_manager.capacity):
            self.queue_manager.queue[i] = None

        # Refill the queue
        self.queue_manager.front = 0
        self.queue_manager.rear = 0
        self.queue_manager.size = 0

        for job in jobs:
            self.queue_manager.queue[self.queue_manager.rear] = job
            self.queue_manager.rear = (self.queue_manager.rear + 1) % self.queue_manager.capacity
            self.queue_manager.size += 1
