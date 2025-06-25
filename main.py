import time
from Job import PrintQueueManager

def main():
    pq = PrintQueueManager(capacity=5)
    print("[MODULE 2] Aging and Priority...")

    print("\n[EVENT] Submitting Job A (priority 1)")
    pq.enqueue_job("user1", "A", priority=1)
    time.sleep(2)

    print("[EVENT] Submitting Job B (priority 2)")
    pq.enqueue_job("user2", "B", priority=2)
    time.sleep(2)

    print("[EVENT] Submitting Job C (priority 1)")
    pq.enqueue_job("user3", "C", priority=1)


    print("\n[STATUS BEFORE AGING]")
    pq.show_status()

    print("\n[WAIT] Sleeping to allow jobs to age...")
    time.sleep(6)  

    print("\n[MODULE 2] Applying priority aging...")
    pq.apply_priority_aging()

    print("\n[STATUS AFTER AGING]")
    pq.show_status()

    print("\n[EVENT] Printing the next job...")
    pq.dequeue_job()

    print("\n[FINAL QUEUE STATUS]")
    pq.show_status()

    print("[MODULE 3] Removing expired jobs...")
    pq.remove_expired_jobs()
    pq.show_status()
if __name__ == "__main__":
    main()