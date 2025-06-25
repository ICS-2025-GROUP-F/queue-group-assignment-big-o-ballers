import time
from Job import PrintQueueManager
from PriorityAging import PriorityAndAgingSystem


def main():
    queue = PrintQueueManager(capacity=5)
    aging_module = PriorityAndAgingSystem(queue, aging_interval=5)  # 5 seconds aging interval

    print("\n[Event] Submitting job1 (P=1)")
    queue.enqueue_job("user1", "job1", priority=1)
    time.sleep(3)

    print("[Event] Submitting job2 (P=2)")
    queue.enqueue_job("user2", "job2", priority=2)
    time.sleep(4)

    print("[Event] Submitting job3 (P=1)")
    queue.enqueue_job("user3", "job3", priority=1)

    queue.show_status()

    print("\n[Tick] Applying priority aging...")
    aging_module.apply_priority_aging()

    queue.show_status()

    time.sleep(6)
    print("\n[Tick] Second aging cycle...")
    aging_module.apply_priority_aging()
    queue.show_status()

if __name__ == "__main__":
    main()