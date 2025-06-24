from PrintQueueManager import PrintQueueManager
#create the queue manager
pq = PrintQueueManager()

#add some jobs to the queue
pq.enqueue_job("User 1","Job001",3)
pq.enqueue_job("User 2","Job002",4)
pq.enqueue_job("User 3","Job003",2)
#simulate time passing
for job in pq.queue:
    job["wait_time"] +=2
    
#show the GUI
pq.show_gui()
