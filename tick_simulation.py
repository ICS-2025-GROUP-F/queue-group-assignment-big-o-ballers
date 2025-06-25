import threading

class PrintQueueManager:
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()

    def tick(self):
        """
        Simulates time passing:
        - Increases waiting time
        - Applies priority aging
        - Removes expired jobs
        - Prints queue snapshot
        """
        with self.lock:
            print("\n⏱ Tick: Advancing time...")

            for job in self.queue[:]:  # Copy to safely remove
                job["waiting_time"] += 1

                # Apply aging
                if job["waiting_time"] % 5 == 0:
                    job["priority"] += 1
                    print(f"🔼 Job {job['job_id']} aged → New priority: {job['priority']}")

                # Expire old jobs
                if job["waiting_time"] >= 15:
                    print(f"❌ Job {job['job_id']} expired and removed.")
                    self.queue.remove(job)

            # Print snapshot
            print("\n📋 Queue Snapshot:")
            if not self.queue:
                print("Queue is empty.")
            else:
                for job in self.queue:
                    print(f"Job {job['job_id']} | Priority: {job['priority']} | Waiting: {job['waiting_time']}")

# Example use
if __name__ == "__main__":
    pq = PrintQueueManager()

    # Add sample jobs
    pq.queue = [
        {"user_id": "U1", "job_id": "J1", "priority": 1, "waiting_time": 0},
        {"user_id": "U2", "job_id": "J2", "priority": 2, "waiting_time": 4},
        {"user_id": "U3", "job_id": "J3", "priority": 1, "waiting_time": 10}
    ]

    # Simulate 20 ticks
    for i in range(20):
        print(f"\n--- Tick {i+1} ---")
        pq.tick()
