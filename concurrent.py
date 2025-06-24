import threading

class PrintQueueManager:
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()

    def enqueue_job(self, user_id, job_id, priority):
        with self.lock:
            print(f"Enqueuing job: {job_id} from user: {user_id} with priority: {priority}")
            self.queue.append({
                "user_id": user_id,
                "job_id": job_id,
                "priority": priority,
                "waiting_time": 0
            })

    def handle_simultaneous_submissions(self, jobs):
        """
        Handle a list of job submissions concurrently.
        Each job is a tuple: (user_id, job_id, priority)
        """
        threads = []

        for user_id, job_id, priority in jobs:
            t = threading.Thread(
                target=self.enqueue_job,
                args=(user_id, job_id, priority)
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print("All simultaneous jobs have been submitted.")

if __name__ == "__main__":
    pq = PrintQueueManager()
    
    job_batch = [
        ("U001", "J001", 2),
        ("U002", "J002", 1),
        ("U003", "J003", 3),
        ("U004", "J004", 2)
    ]
    
    pq.handle_simultaneous_submissions(job_batch)
