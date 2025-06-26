Team: Big-O-Ballers

Members:
    183617	Wayne Kimutai - Module 2 & 3
    181052	Muriu Alfred- Module 4
    184255	Mwendwa Kelvin Muoki- Module 1
    192569	Koima Kipseba Ethan- Module 6
    190165	Denzel Omondi-Module 5

Brief description
    Module 1 (Muoki)
        Implements the core circular queue structure. It supports adding (enqueue_job) and removing (dequeue_job) jobs, while maintaining job metadata such as user ID.

    Module 2(Wayne)
        Implements a priority-based job ordering system. Jobs with higher priority are served first. Also handles aging logic.

    Module 3(Wayne)
        Handles automatic removal of stale jobs. If a job waits in the queue longer than a set threshold.
    
    Module 4(Muriu)
        Allows multiple users to submit jobs at the same time. It ensures that job submission is thread-safe by using synchronization mechanisms.

    Module 5(Denzel)
         Simulates time progression through a tick() function. Each tick updates job waiting times, applies aging and checks for expiry.

    Module 6(Ethan)
        Provides clear snapshots of the queue after every event.
    
IMPLEMENTATION:
    Run main.py