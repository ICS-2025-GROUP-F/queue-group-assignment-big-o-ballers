import tkinter as tk
from tkinter import ttk

from colorama import Fore, Style , init
init(autoreset=True)  # Automatically reset color after each print
class PrintQueueManager:
    def __init__(self):
        self.queue = []  # This will store job dictionaries
        
        
    
    def enqueue_job(self, user_id, job_id, priority):
        job = {
            "user_id": user_id,
            "job_id": job_id,
            "priority": priority,
            "wait_time": 0  # Initial wait time
        }
        self.queue.append(job)
        
    def show_gui(self):
        Window = tk.Tk()
        Window.title("Print Queue Visualization.")
       
        columns = ("Position","User ID", "Job ID", "Priority", "Wait Time")
        tree = ttk.Treeview(Window,columns=columns,show="headings")
        for col in columns:
           tree.heading(col, text = col)
           tree.column(col,width=100)
           
        #Add job data to the table
        for i, job in enumerate(self.queue,start=1):
            tree.insert("","end",values=(i,job["user_id"], job["job_id"], job["priority"], job["wait_time"]))
        tree.pack(padx=10,pady=10)
        Window.mainloop()

    def show_status(self):
        # We'll implement this part next
        if not self.queue:
            print(Fore.RED + "\n--- Print Queue is currently empty ---\n")
            return

        print(Fore.CYAN+"\n--- Current Print Queue Status ---")
        print(Fore.YELLOW+f"{'Position':<10} {'User':<10} {'Job ID':<10} {'Priority':<10} {'Wait Time':<10}")
        print(Fore.YELLOW+"-" * 55)

        for index, job in enumerate(self.queue, start=1):
            print(Fore.GREEN+f"{index:<10} {job['user_id']:<10} {job['job_id']:<10} {job['priority']:<10} {job['wait_time']:<10}")
    
        print(Fore.YELLOW+"-" * 55 + "\n")
        
